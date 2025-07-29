from robocorp import browser
from robocorp.tasks import task

from RPA.HTTP import HTTP
from RPA.PDF import PDF

import pandas as pd
import time as t

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        screenshot="only-on-failure",
        headless=False
    )
    context_page =open_robot_order_website("https://robotsparebinindustries.com/#/robot-order")
    close_modal(context_page)
   
    download_orders_file("https://robotsparebinindustries.com/orders.csv","orders.csv")
    create_pdf_from_folder("ordered_robots","receipts.pdf")
  
   


def open_robot_order_website(url):
    context_page = browser.goto(url)
    return context_page

def download_orders_file(url_file, wb_name):
    http = HTTP()
    http.download(url_file,overwrite=True)
    df = pd.read_csv(wb_name)
    for i in range(len(df)):
        fill_form(df.iloc[i],i)
        
    

def close_modal(context_page: browser.Page):
    context_page.click(".btn-dark")
      

def fill_form(order, i: int):
    context_page = browser.page()
    context_page.wait_for_selector("#head", state="visible")
    context_page.select_option("#head", str(order["Head"]))
    context_page.click("#id-body-"+str(order["Body"]))
    context_page.fill("#address", str(order["Address"]))
    context_page.get_by_placeholder("Enter the part number for the legs").fill(str(order["Legs"]))
    context_page.click("#preview")
    context_page.wait_for_selector("#robot-preview-image", state="visible")
    print_screen(f"ordered_robots/screenshot_{i}.png")
    context_page.click("#order")
    if context_page.is_visible(".alert-danger"):
        context_page.click("#order")
        context_page.wait_for_selector("#order-another", state="visible")
        context_page.click("#order-another")
    else:
        context_page.wait_for_selector("#order-another", state="visible")
        context_page.click("#order-another")
    context_page.click(".btn-dark")
    
def print_screen(screenshot_path: str):
    page = browser.page()
    page.screenshot(path=screenshot_path)

def create_pdf_from_folder(folder_path: str, pdf_path: str):
    import os
    import glob
    
    pdf = PDF()
    # Get all PNG files from the folder
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    
    if png_files:
        # Create PDF from all PNG files
        pdf.open_pdf(pdf_path)
        pdf.add_files_to_pdf(files=png_files, target_document=pdf_path)
        pdf.save_pdf(pdf_path)
        print(f"Created PDF with {len(png_files)} images")
    else:
        print("No PNG files found in the folder")







        

