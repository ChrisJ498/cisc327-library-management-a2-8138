GitHub Repository link: https://github.com/ChrisJ498/cisc327-library-management-a2-8138
Name: Chris Jakubowkski
NetID: 20388138

1. 
I have completed the implentation for the fuctions that required work (R4,R5,R6,R7). 
The implentation was straightforward for the most part. Almost all of the requirements have been fufilled. 
For R7, I did not impliment the website interface

2. 
I created additional test cases for R6 and R7
These additional tests for R6 are: test_search_isbn, test_search_title_partial, test_search_author_partial, test_not_existing_title
These additional tests for R7 are: test_patron_with_books, test_patron_with_invalid_id, test_patron_with_no_books

3. 
I have chosen to use the LLM Google Gemini to generate test cases.
My initial prompt was requesting Gemini to write the test cases and provided it with the neccessary information to properly do so, it is pasted below:
(Line 18-307)


I am designing a website to essentially be a virtual library. I need 5 tests for each of several specific requirements, titled as R1-7
R1: ### R1: Add Book To Catalog
The system shall provide a web interface to add new books to the catalog via a form with the following fields:
- Title (required, max 200 characters)
- Author (required, max 100 characters)
- ISBN (required, exactly 13 digits)
- Total copies (required, positive integer)
- The system shall display success/error messages and redirect to the catalog view after successful addition.
def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

R2:
### R2: Book Catalog Display
The system shall display all books in the catalog in a table format showing:
- Book ID, Title, Author, ISBN
- Available copies / Total copies
- Actions (Borrow button for available books)

R3:
### R3: Book Borrowing Interface
The system shall provide a borrowing interface to borrow books by patron ID:

- Accepts patron ID and book ID as the form parameters
- Validates patron ID (6-digit format)
- Checks book availability and patron borrowing limits (max 5 books)
- Creates borrowing record and updates available copies
- Displays appropriate success/error messages
def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

R4:
### R4: Book Return Processing
The system shall provide a return interface that includes:

- Accepts patron ID and book ID as form parameters
- Verifies the book was borrowed by the patron
- Updates available copies and records return date
- Calculates and displays any late fees owed
def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    TODO: Implement R4 as per requirements
    
    return False, "Book return functionality is not yet implemented."
    """

    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    # Check if patron borrowed book
    borrowed_books = get_patron_borrowed_books(patron_id)
    borrowed_book_ids = [i["book_id"] for i in borrowed_books]
    if book_id not in borrowed_book_ids:
        return False, "No borrow record found for this book and patron."
    
    #Update book availability
    availability_success = update_book_availability(book_id, +1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."

    # Record Return Date
    return_date = datetime.now()
    #Update borrow record
    update_success = update_borrow_record_return_date(patron_id, book_id, return_date)
    if not update_success:
        return False, "Database error occurred while creating borrow record."\
    
    #Determine late fee
    late_fee = calculate_late_fee_for_book(patron_id, book_id)
    fee_amount = late_fee["fee amount"]
    days_overdue = late_fee["days_overdue"]
    
    #Display overdue information
    if days_overdue > 0:
        message = "Book returned is " + str(days_overdue) + " days late and you owe $" + str(fee_amount)
        return True, message
    else:
        message = "Book returned on time"
        return True, message
        

R5:
### R5: Late Fee Calculation API
The system shall provide an API endpoint GET `/api/late_fee/<patron_id>/<book_id>` that includes the following.
- Calculates late fees for overdue books based on:
  - Books due 14 days after borrowing
  - $0.50/day for first 7 days overdue
  - $1.00/day for each additional day after 7 days
  - Maximum $15.00 per book
- Returns JSON response with fee amount and days overdue
def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 
    
    
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """

    #check if book was borrowed
    borrowed_books = get_patron_borrowed_books(patron_id)
    borrowed_book_ids = [i["book_id"] for i in borrowed_books]
    if book_id not in borrowed_book_ids:
        return False, "No borrow record found for this book and patron."
    
    #Find the book
    book_borrowed = None
    for i in borrowed_books:
        if i["book_id"] == book_id:
            book_borrowed = i
            break

    #Find how many days late
    days_overdue = (datetime.now - book_borrowed["due_date"]).days

    #Determine fee amount
    fee_amount = 0.0    
    if days_overdue <= 7:
        fee_amount = days_overdue * 0.5
    else: 
        fee_amount = 7 * 0.5 + (days_overdue - 7) * 1.0
    if fee_amount > 15.0:
        fee_amount = 15.0

    #Return results
    return {
        'fee_amount': fee_amount,
        'days_overdue': days_overdue,
        'status': "Late fee calculated"
    }


R6:
### R6: Book Search Functionality
The system shall provide search functionality with the following parameters:
- `q`: search term
- `type`: search type (title, author, isbn)
- Support partial matching for title/author (case-insensitive)
- Support exact matching for ISBN
- Return results in same format as catalog display
def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    
    TODO: Implement R6 as per requirements
    """

    results = []

    if search_type == 'isbn':
        results.append(get_book_by_isbn(search_term))

    else:
        all_books = get_all_books()
        for i in all_books:
            if search_type == 'title' and search_term.lower() in i['title'].lower():
                results.append(i)
            elif search_type == 'author' and search_term.lower() in i['author'].lower():
                results.append(i)
    
    return results

R7:
### R7: Patron Status Report 

The system shall display patron status for a particular patron that includes the following: 

- Currently borrowed books with due dates
- Total late fees owed  
- Number of books currently borrowed
- Borrowing history
def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """

    status_report = {}

    borrowed_books = get_patron_borrowed_books(patron_id)
    status_report['current_borrowed'] = borrowed_books

    total_late_fees = 0.0
    for i in borrowed_books:
        fees = calculate_late_fee_for_book(patron_id, i['book_id'])
        total_late_fees += fees('fee_amount')
    status_report['total_late_fees'] = total_late_fees

    status_report['total_books_borrowed'] = get_patron_borrow_count(patron_id)

    #Borrow_records mentioned in database
    status_report['borrowing_history'] = borrowed_books

    return status_report


This resulted in Gemini describing test cases in pseudo-python, so I sent a follow-up message saying "Write the test cases as actual code".
After this message, Gemini first gave a mock-implentation of required code, and then followed it with the test cases pasted below:
(Line 314-669)

# --- TEST CLASSES ---

class TestR1AddBookToCatalog(unittest.TestCase):
    
    def setUp(self):
        self.mock_get_book_by_isbn = MagicMock()
        self.mock_insert_book = MagicMock(return_value=True)
        self.long_title = "A" * 200
        self.long_author = "B" * 100

    def test_1_successful_book_addition_max_lengths(self):
        # Test 1: Successful Book Addition (Boundary: Max Lengths)
        self.mock_get_book_by_isbn.return_value = None
        result, message = add_book_to_catalog(self.long_title, self.long_author, "1234567890123", 1, self.mock_get_book_by_isbn, self.mock_insert_book)
        self.assertTrue(result)
        self.assertIn("successfully added", message)
        self.mock_insert_book.assert_called_once()

    def test_2_title_required_check(self):
        # Test 2: Title Required/Empty Check
        result, message = add_book_to_catalog("", self.long_author, "9876543210987", 5, self.mock_get_book_by_isbn, self.mock_insert_book)
        self.assertFalse(result)
        self.assertEqual("Title is required.", message)

    def test_3_isbn_length_check_too_short(self):
        # Test 3: ISBN Length Check (Too Short)
        result, message = add_book_to_catalog("Short Title", "Jane Doe", "123456789012", 5, self.mock_get_book_by_isbn, self.mock_insert_book)
        self.assertFalse(result)
        self.assertEqual("ISBN must be exactly 13 digits.", message)

    def test_4_total_copies_validation_non_positive(self):
        # Test 4: Total Copies Validation (Non-Positive)
        result, message = add_book_to_catalog("Test Book", "Test Author", "1111111111111", 0, self.mock_get_book_by_isbn, self.mock_insert_book)
        self.assertFalse(result)
        self.assertEqual("Total copies must be a positive integer.", message)
        
    def test_5_duplicate_isbn_check(self):
        # Test 5: Duplicate ISBN Check
        self.mock_get_book_by_isbn.return_value = {"title": "Existing Book"} # Mocking an existing book
        result, message = add_book_to_catalog("New Title", "New Author", "9999999999999", 2, self.mock_get_book_by_isbn, self.mock_insert_book)
        self.assertFalse(result)
        self.assertEqual("A book with this ISBN already exists.", message)

# R2 is a UI/Acceptance test, cannot be implemented as a unit test for the provided function signatures.

class TestR3BookBorrowing(unittest.TestCase):
    
    def setUp(self):
        self.mock_get_book_by_id = MagicMock()
        self.mock_get_patron_borrow_count = MagicMock()
        self.mock_insert_borrow_record = MagicMock(return_value=True)
        self.mock_update_book_availability = MagicMock(return_value=True)

    def test_1_successful_borrowing(self):
        # Test 1: Successful Borrowing
        self.mock_get_book_by_id.return_value = {"title": "Test Book", "available_copies": 2}
        self.mock_get_patron_borrow_count.return_value = 3
        result, message = borrow_book_by_patron("123456", 5, self.mock_get_book_by_id, self.mock_get_patron_borrow_count, self.mock_insert_borrow_record, self.mock_update_book_availability)
        self.assertTrue(result)
        self.assertIn("Successfully borrowed \"Test Book\"", message)
        self.mock_insert_borrow_record.assert_called_once()
        self.mock_update_book_availability.assert_called_once_with(5, -1)

    def test_2_invalid_patron_id_non_digit(self):
        # Test 2: Invalid Patron ID (Non-Digit)
        result, message = borrow_book_by_patron("A12345", 1, self.mock_get_book_by_id, self.mock_get_patron_borrow_count, self.mock_insert_borrow_record, self.mock_update_book_availability)
        self.assertFalse(result)
        self.assertEqual("Invalid patron ID. Must be exactly 6 digits.", message)

    def test_3_book_unavailable_zero_copies(self):
        # Test 3: Book Unavailable (Zero Copies)
        self.mock_get_book_by_id.return_value = {"title": "Unavailable Book", "available_copies": 0}
        self.mock_get_patron_borrow_count.return_value = 1
        result, message = borrow_book_by_patron("123456", 2, self.mock_get_book_by_id, self.mock_get_patron_borrow_count, self.mock_insert_borrow_record, self.mock_update_book_availability)
        self.assertFalse(result)
        self.assertEqual("This book is currently not available.", message)

    def test_4_maximum_borrowing_limit_reached(self):
        # Test 4: Maximum Borrowing Limit Reached
        self.mock_get_book_by_id.return_value = {"title": "Available Book", "available_copies": 1}
        self.mock_get_patron_borrow_count.return_value = 5 # Should fail because >= 5
        result, message = borrow_book_by_patron("999999", 3, self.mock_get_book_by_id, self.mock_get_patron_borrow_count, self.mock_insert_borrow_record, self.mock_update_book_availability)
        self.assertFalse(result)
        self.assertEqual("You have reached the maximum borrowing limit of 5 books.", message)

    def test_5_book_not_found(self):
        # Test 5: Book Not Found
        self.mock_get_book_by_id.return_value = None
        self.mock_get_patron_borrow_count.return_value = 1
        result, message = borrow_book_by_patron("123456", 99, self.mock_get_book_by_id, self.mock_get_patron_borrow_count, self.mock_insert_borrow_record, self.mock_update_book_availability)
        self.assertFalse(result)
        self.assertEqual("Book not found.", message)

class TestR4BookReturnProcessing(unittest.TestCase):
    
    def setUp(self):
        # Mocks for R4 dependencies
        self.mock_get_book_by_id = MagicMock(return_value={"id": 5, "title": "Test Book"})
        self.mock_get_patron_borrowed_books = MagicMock()
        self.mock_update_book_availability = MagicMock(return_value=True)
        self.mock_update_borrow_record_return_date = MagicMock(return_value=True)
        self.mock_calculate_late_fee_for_book = MagicMock()
        
        # Borrowed book structure for mocks
        self.borrowed_book_record = [
            {"book_id": 5, "patron_id": "123456", "due_date": datetime.now() - timedelta(days=5)}
        ]

    def test_1_successful_on_time_return(self):
        # Test 1: Successful On-Time Return
        self.mock_get_patron_borrowed_books.return_value = self.borrowed_book_record
        self.mock_calculate_late_fee_for_book.return_value = {"days_overdue": 0, "fee amount": 0.00}
        result, message = return_book_by_patron_mocked("123456", 5, 
                                                       self.mock_get_book_by_id, self.mock_get_patron_borrowed_books, 
                                                       self.mock_update_book_availability, self.mock_update_borrow_record_return_date, 
                                                       self.mock_calculate_late_fee_for_book)
        self.assertTrue(result)
        self.assertEqual("Book returned on time", message)
        self.mock_update_book_availability.assert_called_once_with(5, 1)

    def test_2_successful_late_return_with_fee(self):
        # Test 2: Successful Late Return with Fee
        self.mock_get_book_by_id.return_value = {"id": 8, "title": "Late Book"}
        self.mock_get_patron_borrowed_books.return_value = [{"book_id": 8, "patron_id": "987654"}]
        self.mock_calculate_late_fee_for_book.return_value = {"days_overdue": 10, "fee amount": 6.50}
        result, message = return_book_by_patron_mocked("987654", 8, 
                                                       self.mock_get_book_by_id, self.mock_get_patron_borrowed_books, 
                                                       self.mock_update_book_availability, self.mock_update_borrow_record_return_date, 
                                                       self.mock_calculate_late_fee_for_book)
        self.assertTrue(result)
        self.assertEqual("Book returned is 10 days late and you owe $6.5", message)

    def test_3_invalid_patron_id_too_short(self):
        # Test 3: Invalid Patron ID (Too Short)
        result, message = return_book_by_patron_mocked("12345", 1, 
                                                       self.mock_get_book_by_id, self.mock_get_patron_borrowed_books, 
                                                       self.mock_update_book_availability, self.mock_update_borrow_record_return_date, 
                                                       self.mock_calculate_late_fee_for_book)
        self.assertFalse(result)
        self.assertEqual("Invalid patron ID. Must be exactly 6 digits.", message)

    def test_4_book_not_borrowed_by_patron(self):
        # Test 4: Book Not Borrowed by Patron
        self.mock_get_book_by_id.return_value = {"id": 7, "title": "Other Book"}
        self.mock_get_patron_borrowed_books.return_value = [{"book_id": 1}, {"book_id": 2}]
        result, message = return_book_by_patron_mocked("555555", 7, 
                                                       self.mock_get_book_by_id, self.mock_get_patron_borrowed_books, 
                                                       self.mock_update_book_availability, self.mock_update_borrow_record_return_date, 
                                                       self.mock_calculate_late_fee_for_book)
        self.assertFalse(result)
        self.assertEqual("No borrow record found for this book and patron.", message)

    def test_5_book_not_found(self):
        # Test 5: Book Not Found
        self.mock_get_book_by_id.return_value = None
        result, message = return_book_by_patron_mocked("123456", 99, 
                                                       self.mock_get_book_by_id, self.mock_get_patron_borrowed_books, 
                                                       self.mock_update_book_availability, self.mock_update_borrow_record_return_date, 
                                                       self.mock_calculate_late_fee_for_book)
        self.assertFalse(result)
        self.assertEqual("Book not found.", message)


class TestR5LateFeeCalculation(unittest.TestCase):
    
    def setUp(self):
        self.mock_get_patron_borrowed_books = MagicMock()
        # Due date is 14 days after today for a clean test setup base
        self.base_due_date = datetime(2025, 1, 14, 10, 0, 0)
        self.patron_id = "123456"
        self.book_id = 1
        self.borrowed_record = [
            {"book_id": self.book_id, "due_date": self.base_due_date}
        ]
        self.mock_get_patron_borrowed_books.return_value = self.borrowed_record

    def calculate_fee(self, days_overdue_offset):
        current_time = self.base_due_date + timedelta(days=days_overdue_offset, hours=1) # +1 hour to ensure days calculation works
        return calculate_late_fee_for_book_functional(self.patron_id, self.book_id, self.mock_get_patron_borrowed_books, current_time)

    def test_1_on_time_return(self):
        # Test 1: On-Time/Early Return (0 days overdue)
        fee_data = self.calculate_fee(days_overdue_offset=-5)
        self.assertEqual(0.00, fee_data['fee_amount'])
        self.assertEqual(0, fee_data['days_overdue'])

    def test_2_first_tier_fee_exactly_7_days_late(self):
        # Test 2: First Tier Fee (Exactly 7 Days Late) -> 7 * $0.50 = $3.50
        fee_data = self.calculate_fee(days_overdue_offset=7)
        self.assertEqual(3.50, fee_data['fee_amount'])
        self.assertEqual(7, fee_data['days_overdue'])

    def test_3_second_tier_fee_10_days_late(self):
        # Test 3: Second Tier Fee (10 Days Late) -> (7 * $0.50) + (3 * $1.00) = $3.50 + $3.00 = $6.50
        fee_data = self.calculate_fee(days_overdue_offset=10)
        self.assertEqual(6.50, fee_data['fee_amount'])
        self.assertEqual(10, fee_data['days_overdue'])

    def test_4_maximum_fee_cap_18_days_late(self):
        # Test 4: Maximum Fee Cap (18 Days Late) -> (7 * $0.50) + (11 * $1.00) = $3.50 + $11.00 = $14.50 (Under cap)
        fee_data = self.calculate_fee(days_overdue_offset=18)
        self.assertEqual(14.50, fee_data['fee_amount'])
        self.assertEqual(18, fee_data['days_overdue'])

    def test_5_fee_capped_30_days_late(self):
        # Test 5: Fee Capped (30 Days Late) -> (7 * $0.50) + (23 * $1.00) = $26.50 (Capped at $15.00)
        fee_data = self.calculate_fee(days_overdue_offset=30)
        self.assertEqual(15.00, fee_data['fee_amount'])
        self.assertEqual(30, fee_data['days_overdue'])

class TestR6BookSearchFunctionality(unittest.TestCase):

    def setUp(self):
        self.mock_get_book_by_isbn = MagicMock()
        self.mock_get_all_books = MagicMock()
        self.catalog = [
            {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "1111111111111"},
            {"id": 2, "title": "Gatsby's Sister", "author": "Jane Doe", "isbn": "2222222222222"},
            {"id": 3, "title": "Book Title", "author": "J.R.R. Tolkien", "isbn": "3333333333333"},
        ]
        self.mock_get_all_books.return_value = self.catalog
        
    def test_1_title_partial_match_case_insensitive(self):
        # Test 1: Title Partial Match (Case Insensitive)
        results = search_books_in_catalog("gats", "title", self.mock_get_book_by_isbn, self.mock_get_all_books)
        self.assertEqual(2, len(results))
        self.assertIn(self.catalog[0], results)
        self.assertIn(self.catalog[1], results)
        
    def test_2_author_partial_match(self):
        # Test 2: Author Partial Match
        results = search_books_in_catalog("tolk", "author", self.mock_get_book_by_isbn, self.mock_get_all_books)
        self.assertEqual(1, len(results))
        self.assertIn(self.catalog[2], results)
        
    def test_3_isbn_exact_match(self):
        # Test 3: ISBN Exact Match
        self.mock_get_book_by_isbn.return_value = self.catalog[0]
        results = search_books_in_catalog("1111111111111", "isbn", self.mock_get_book_by_isbn, self.mock_get_all_books)
        self.assertEqual(1, len(results))
        self.assertEqual(self.catalog[0], results[0])

    def test_4_isbn_partial_match_should_fail(self):
        # Test 4: ISBN Partial Match (Should Fail)
        self.mock_get_book_by_isbn.return_value = None # ISBN search must be exact
        results = search_books_in_catalog("111111111", "isbn", self.mock_get_book_by_isbn, self.mock_get_all_books)
        self.assertEqual(0, len(results))
        
    def test_5_no_matches_found(self):
        # Test 5: No Matches Found
        results = search_books_in_catalog("XYZNonexistent", "title", self.mock_get_book_by_isbn, self.mock_get_all_books)
        self.assertEqual(0, len(results))

class TestR7PatronStatusReport(unittest.TestCase):
    
    def setUp(self):
        self.mock_get_patron_borrowed_books = MagicMock()
        self.mock_calculate_late_fee_for_book = MagicMock()
        self.mock_get_patron_borrow_count = MagicMock()
        self.patron_id = "123456"

    def test_1_full_report_generation(self):
        # Test 1: Full Report Generation (On-Time & Late Books)
        book_a = {"book_id": 10, "title": "Book A", "due_date": datetime.now()}
        book_b = {"book_id": 11, "title": "Book B", "due_date": datetime.now()}
        book_c = {"book_id": 12, "title": "Book C", "due_date": datetime.now()}
        
        self.mock_get_patron_borrowed_books.return_value = [book_a, book_b, book_c]
        self.mock_get_patron_borrow_count.return_value = 3
        
        # Mock late fees: Book A (0), Book B (1.00), Book C (6.50)
        def side_effect_fee(patron, book_id):
            if book_id == 10: return {'fee_amount': 0.00, 'days_overdue': 0}
            if book_id == 11: return {'fee_amount': 1.00, 'days_overdue': 2}
            if book_id == 12: return {'fee_amount': 6.50, 'days_overdue': 10}
            return {'fee_amount': 0.00, 'days_overdue': 0}

        self.mock_calculate_late_fee_for_book.side_effect = side_effect_fee
        
        report = get_patron_status_report_mocked(self.patron_id, 
                                                 self.mock_get_patron_borrowed_books, 
                                                 self.mock_calculate_late_fee_for_book, 
                                                 self.mock_get_patron_borrow_count)
        
        self.assertEqual(3, len(report['current_borrowed']))
        self.assertEqual(7.50, report['total_late_fees']) # 0.00 + 1.00 + 6.50
        self.assertEqual(3, report['total_books_borrowed'])
        self.assertEqual(report['current_borrowed'], report['borrowing_history'])

    def test_2_patron_with_no_borrowed_books(self):
        # Test 2: Patron with No Borrowed Books
        self.mock_get_patron_borrowed_books.return_value = []
        self.mock_get_patron_borrow_count.return_value = 0
        self.mock_calculate_late_fee_for_book.return_value = {'fee_amount': 0.00} # Should not be called
        
        report = get_patron_status_report_mocked("000000", 
                                                 self.mock_get_patron_borrowed_books, 
                                                 self.mock_calculate_late_fee_for_book, 
                                                 self.mock_get_patron_borrow_count)

        self.assertEqual([], report['current_borrowed'])
        self.assertEqual(0.00, report['total_late_fees'])
        self.assertEqual(0, report['total_books_borrowed'])

    def test_3_total_late_fees_calculation_check_max_fee_cap(self):
        # Test 3: Total Late Fees Calculation Check (Max Fee Cap)
        book_x = {"book_id": 20, "title": "Book X"}
        book_y = {"book_id": 21, "title": "Book Y"}
        self.mock_get_patron_borrowed_books.return_value = [book_x, book_y]
        self.mock_get_patron_borrow_count.return_value = 2

        # Mock late fees: Book X ($15.00 max fee), Book Y ($3.50 fee)
        def side_effect_fee(patron, book_id):
            if book_id == 20: return {'fee_amount': 15.00, 'days_overdue': 30}
            if book_id == 21: return {'fee_amount': 3.50, 'days_overdue': 7}
            return {'fee_amount': 0.00, 'days_overdue': 0}
        
        self.mock_calculate_late_fee_for_book.side_effect = side_effect_fee

        report = get_patron_status_report_mocked("777777", 
                                                 self.mock_get_patron_borrowed_books, 
                                                 self.mock_calculate_late_fee_for_book, 
                                                 self.mock_get_patron_borrow_count)
        
        self.assertEqual(18.50, report['total_late_fees']) # 15.00 + 3.50

    def test_4_total_books_borrowed_matches_current_borrowed(self):
        # Test 4: total_books_borrowed Matches current_borrowed
        five_books = [{"book_id": i} for i in range(5)]
        self.mock_get_patron_borrowed_books.return_value = five_books
        self.mock_get_patron_borrow_count.return_value = 5
        self.mock_calculate_late_fee_for_book.return_value = {'fee_amount': 0.00}
        
        report = get_patron_status_report_mocked("888888", 
                                                 self.mock_get_patron_borrowed_books, 
                                                 self.mock_calculate_late_fee_for_book, 
                                                 self.mock_get_patron_borrow_count)

        self.assertEqual(5, len(report['current_borrowed']))
        self.assertEqual(5, report['total_books_borrowed'])

    def test_5_invalid_patron_id_handling_no_data(self):
        # Test 5: Invalid Patron ID Handling (Sub-functions return no data)
        self.mock_get_patron_borrowed_books.return_value = []
        self.mock_get_patron_borrow_count.return_value = 0
        self.mock_calculate_late_fee_for_book.reset_mock() # Ensure it's not called on empty list
        
        report = get_patron_status_report_mocked("invalid_id", 
                                                 self.mock_get_patron_borrowed_books, 
                                                 self.mock_calculate_late_fee_for_book, 
                                                 self.mock_get_patron_borrow_count)

        self.assertEqual([], report['current_borrowed'])
        self.assertEqual(0.00, report['total_late_fees'])
        self.assertEqual(0, report['total_books_borrowed'])
        self.mock_calculate_late_fee_for_book.assert_not_called() # Should not call fee calculation on an empty list


4. 
R1:
Both mine and Gemini's test cases covered a similar variety of different cases, Gemini's covered edge cases while mine did not

R2:
Neither Gemini or I produced test cases for R2

R3:
Both were similar in covering specific scenarios, but I feel Gemini had a better range of coverage as well as covering the edge cases

R4:
My test cases covered more scenarios involving error through user input while Gemini was more based on involving other functions involved such as late fees and was overall more in depth

R5:
Gemini was solely focused on the calculation of the late fee and had no testing on the invalid inputs, while my tests had the inputs being involved. Gemini had testing on edge cases while I did not

R6:
Both test suites were similar in coverage for this requirment. Both convered a similar variety of scenarios

R7:
Both were similar except Gemini had a test case on late fees while mine did not.

Overall, Gemini had a wider range of coverage specifically in regards to covering edge cases. Gemini produced seemingly high quality test cases with a solid amount of coverage.