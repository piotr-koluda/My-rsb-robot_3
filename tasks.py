from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.FileSystem import FileSystem
import time
import shutil



URL = "https://robotsparebinindustries.com/"
csv_file = "https://robotsparebinindustries.com/orders.csv"
file_name = "orders.csv"
destination_folder = "output\\reciepts\\"

@task
def order_robots_from_Robotsparebin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    download_file(csv_file)
    table = read_csv_file(file_name)
    open_robot_order_website(URL=URL)
    time.sleep(1)

    archive_path = "output\\archive\\"
    create_dictionary(archive_path)

    for row in table:
        close_annoying_popup()
        fill_order(row)
        pdf_file = store_receipt_as_pdf(row['Order number'], destination_folder=destination_folder)
        screen_file = take_screenshot(row['Order number'], path_to_save=destination_folder)
        combine_pdfs(order_path=screen_file,receipte_path=pdf_file, archive_path=archive_path+row['Order number']+".pdf")
        order_another_robot()
    

    archive_receipts(destination_folder
                     , archive_path)
        

    close_page()
def create_dictionary(path:str):
    FileSystem.create_directory(FileSystem, path,parents=True,exist_ok=True)


def download_file(file_to_download: str):
    file = HTTP()
    file.download(url=file_to_download, overwrite=True)

def read_csv_file(name_file: str):
    table = Tables()
    return table.read_table_from_csv(name_file)

def order_another_robot():
    page = browser.page()
    page.locator("#order-another").click()

def close_annoying_popup():
    page = browser.page()
    page.locator(".btn-dark").click()


def open_robot_order_website(URL:str):
    browser.configure(
        slowmo = 50
    )
    browser.goto(url=URL)
    page = browser.page()
    page.locator(".nav-item:nth-child(2) > .nav-link").click()
    page.locator(".modal-header").wait_for()
    

def store_receipt_as_pdf(order_number: str, destination_folder: str):
    destination_path = destination_folder+order_number+".pdf"
    page = browser.page()
    receipte_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(receipte_html, destination_path)
    return destination_path

def fill_order(row):
    page = browser.page()
    page.locator("xpath=//select[@id='head']").select_option(row['Head'])
    page.locator(".radio:nth-child("+row['Body']+") > label").click()
    page.locator("xpath=//label[contains(.,'3. Legs:')]/../input").fill(row['Legs'])
    page.locator("#address").fill(row['Address'])
    page.locator("xpath=//button[contains(.,'Show model info')]").click()
    while page.locator("#order").is_visible(timeout=0.001):
        page.locator("#order").click()

    """ page.locator("#order").click()
    time.sleep(0.03)
    alert_popup = page.locator("#order").is_visible
    if alert_popup:
        page.locator("#order").click()
 """
    
def take_screenshot(order_number: str, path_to_save: str):
    destination_path = path_to_save+order_number+".png"
    page = browser.page()
    page.locator("xpath=//*[@id='robot-preview-image']").screenshot(path=destination_path)
    return destination_path

def combine_pdfs(order_path: str , receipte_path: str, archive_path:str):
    list_of_files =[order_path, receipte_path]
    pdf = PDF()
    pdf.add_files_to_pdf(list_of_files, target_document=archive_path)


def archive_receipts(folder_path:str, directory: str ):
    file_paht_zip = folder_path+"archive"
    shutil.make_archive(base_name=file_paht_zip, format="zip", root_dir=directory)
    """ tekst """


def close_page():
    page = browser.page()
    page.close()

    # TODO: add launching robot and login to page
