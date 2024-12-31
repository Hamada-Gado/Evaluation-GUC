from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchDriverException
from selenium.common.exceptions import NoSuchWindowException


def main():
    drivers: list[type[RemoteWebDriver]] = [
        webdriver.Safari,
        webdriver.Edge,
        webdriver.Firefox,
        webdriver.Chrome,
    ]

    driver = None
    while driver is None:
        try:
            driver = drivers.pop()()
        except NoSuchDriverException:
            if len(drivers) == 0:
                raise Exception(
                    "No webdrivers were found. Please install a webdriver and try again."
                )
            continue
    driver.get("https://apps.guc.edu.eg/student_ext/Evaluation/EvaluateStaff.aspx")

    input("Please login to your account and press enter to continue")

    dropdown_list = driver.find_element(
        By.CSS_SELECTOR, "#ContentPlaceHolderright_ContentPlaceHoldercontent_stfIdLst"
    )

    # get number of Staff Members
    # -1 to exclude the first option which is "Choose Staff Member"
    len_options = len(dropdown_list.find_elements(By.TAG_NAME, "option")) - 1

    for option in range(len_options):
        # Wait for the dropdown list to appear

        while True:
            try:
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.find_element(
                        By.CSS_SELECTOR,
                        "#ContentPlaceHolderright_ContentPlaceHoldercontent_stfIdLst",
                    )
                )
                break
            except TimeoutException:
                print("TimeoutException occured, the page is taking too long to load")
                print("Press enter to try again or Ctrl+C to exit")
                input()

        # select staff member
        dropdown_list = driver.find_element(
            By.CSS_SELECTOR,
            "#ContentPlaceHolderright_ContentPlaceHoldercontent_stfIdLst",
        )
        dropdown_list.find_elements(By.TAG_NAME, "option")[option + 1].click()

        # if the staff member is already evaluated, skip to the next staff member
        if (
            driver.find_element(
                By.CSS_SELECTOR,
                "#ContentPlaceHolderright_ContentPlaceHoldercontent_msgLbl",
            ).text
            != ""
        ):
            continue

        while True:
            try:
                # Wait for the agree radio button to appear
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.find_element(
                        By.CSS_SELECTOR,
                        "#ContentPlaceHolderright_ContentPlaceHoldercontent_objRptr_grade_0_1_0",
                    )
                )
                break
            except TimeoutException:
                print("TimeoutException occured, the page is taking too long to load")
                print("Press enter to try again or Ctrl+C to exit")
                input()

        for i in range(14):
            # agree radio button
            driver.find_element(
                By.CSS_SELECTOR,
                f"#ContentPlaceHolderright_ContentPlaceHoldercontent_objRptr_grade_{i}_1_{i}",
            ).click()

        # post button
        driver.find_element(
            By.CSS_SELECTOR,
            "#ContentPlaceHolderright_ContentPlaceHoldercontent_pstEvalBtn",
        ).click()

    input("Press enter to exit")

    # Try to quit the driver. If there is an error, ignore it.
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except NoSuchWindowException:
        print("The browser window was closed. Exiting...")
