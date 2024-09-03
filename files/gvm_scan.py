import argparse
import os
import time
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
import xml.etree.ElementTree as ET

#Constants
#This settings are persisted across all Greenbone versions and their values never change
CONFIG_ID = 'daba56c8-73ec-11df-a475-002264764cea'  # Full and Fast Scan Config
SCANNER_ID = '08b69003-5fc2-4037-a479-93b440211c73' # Default openvas scanner id
PORTS_ID = '730ef368-57e2-11e1-a90f-406186ea4fc5' # All TCP and Nmap top 100 UDP
REPORT_FORMAT_ID = 'a994b278-1f62-11e1-96ac-406186ea4fc5' # XML report format

def create_target(gmp, name, host, port_list_id):
    response = gmp.create_target(name=name, hosts=[host], port_list_id=port_list_id)
    # Parse the XML response to extract the 'id' attribute and return   
    return ET.fromstring(response).attrib['id']

def create_task(gmp, name, config_id, target_id, scanner_id):
    response = gmp.create_task(name=name, config_id=config_id, target_id=target_id, scanner_id=scanner_id)
    # Parse the XML response to extract the 'id' attribute and return  
    return ET.fromstring(response).attrib['id']

def start_task(gmp, task_id):
    response = gmp.start_task(task_id)
    return ET.fromstring(response).find('.//report_id').text

def get_task_status(gmp, task_id):
    response = gmp.get_task(task_id)
    task_xml = ET.fromstring(response)
    return task_xml.find('.//status').text

def wait_for_task_completion(gmp, task_id, timeout=14400):  # Extended timeout for long scans
    # NOTE(90n20): greenbone tasks timeout has been doubled as tests showed that some domains took more than 2 hours to be completed
    print(f"Task {task_id}: Waiting for completion.")
    start_time = time.time()
    while True:
        status = get_task_status(gmp, task_id)
        if status in ['Done', 'Stopped', 'Interrupted']:
            print(f"Task {task_id} completed with status: {status}")
            return status
        elif time.time() - start_time > timeout:
            raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds.")
        print(f"Task {task_id} status: {status}. Checking again in 5 minutes.")
        time.sleep(300)  # Check every 5 minutes

def get_report(gmp, reports_dir: str, report_id):
    response = gmp.get_report(report_id=report_id, report_format_id=REPORT_FORMAT_ID)
    report_content = ET.fromstring(response).find('report')
    report_filename = f'report_{report_id}.xml'
    output_file = os.path.join(reports_dir, report_filename)
    with open(output_file, 'wb') as file:
        file.write(ET.tostring(report_content, encoding='utf8', method='html'))
    print(f"Report saved as {report_filename}")
    print(ET.tostring(report_content, encoding='utf8'))
    return report_filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", action="append")
    parser.add_argument("--reports-dir", type=str)
    args = parser.parse_args()
    connection = UnixSocketConnection(path='/tmp/gvm/gvmd/gvmd.sock')
    with Gmp(connection) as gmp:
        gmp.authenticate('admin', 'admin')

        for target in args.target:
            print(f"Creating target and task for {target}")
            target_id = create_target(gmp, f'Target for {target}', target, PORTS_ID)
            task_id = create_task(gmp, f'Scan for {target}', CONFIG_ID, target_id, SCANNER_ID)
            print(f"Starting task {task_id} for target {target_id}")
            report_id = start_task(gmp, task_id)
            print(f"Task {task_id} corresponding report => {report_id}")
            final_status = wait_for_task_completion(gmp, task_id)
            if final_status == 'Done':
                get_report(gmp, args.reports_dir, report_id)

if __name__ == '__main__':
    main()
