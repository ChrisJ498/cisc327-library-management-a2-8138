import pytest
import random
from playwright.sync_api import Page, expect

def test_add_new_book(page: Page):
    #Testing for adding a new book

    #Creating a new title/isbn when testing
    test_isbn = f"{random.randint(1000000000000, 9999999999999)}"
    test_title = f"Test Book {test_isbn}"

    page.goto("http://localhost:5000")

    page.get_by_text("Add Book").click()

    page.fill('input[name="title"]', test_title)
    page.fill('input[name="author"]', "Test Author")
    page.fill('input[name="isbn"]', test_isbn)
    page.fill('input[name="total_copies"]', "5")

    page.get_by_role("button", name="Add Book to Catalog").click()

    expect(page.get_by_text(f'Book "{test_title}" has been successfully added to the catalog.')).to_be_visible()

def test_search_for_book(page: Page):
    #Testing for searching for a book by its title
    page.goto("http://localhost:5000")

    page.get_by_text("Search").click()

    page.fill('input[name="q"]', "Great Gatsby")
    page.select_option('select[name="type"]', label="Title (partial match)")

    page.get_by_role("button", name="Search").click()

    expect(page.get_by_text("The Great Gatsby")).to_be_visible()