<!--
# Required libraries

pip install django
pip install django-ninja
pip install pillow
pip install qrcode
-->

# Brevis

Brevis is a high-performance URL shortener API built with Python and Django, leveraging the Ninja framework for efficient API development. It provides a simple and intuitive interface for creating, retrieving, updating, and tracking shortened URLs.

## Key Features

* **URL Shortening:** Create concise short URLs for any given long URL.

* **QR Code Generation:** Generate QR codes for easy sharing of shortened links.

* **Link Tracking:** Track key metrics such as total clicks, unique clicks, and click history.

* **Customizable Expiration:** Set expiration times for your shortened links.

* **User-Friendly API:** Clean and well-documented API for easy integration with other applications.

* **Scalable and Maintainable:** Built with a focus on scalability and maintainability for future growth.

## Technologies Used

* **Python:** The core programming language.

* **Django:** A high-level web framework for rapid development.

* **Ninja:** A modern and performant API framework for Django.

* **PostgreSQL:** (Recommended) A robust and scalable database for storing link data.

## Installation

1. Clone the repository:

    ```
    git clone <repository_url>
    ```

2. Create a virtual environment:  

    ```
    python -m venv venv
    source venv/bin/activate  # On Unix-like systems
    venv\Scripts\activate      # On Windows
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Configure database settings:

    * Create a PostgreSQL database (if not already created).

    * Update the `DATABASE_URL` setting in `brevis/settings.py` with your database credentials.

5. Run migrations:

    ```
    python manage.py migrate
    ```

6. Start the development server:

    ```
    python manage.py runserver
    ```

## Usage

Refer to the API documentation for detailed information on available endpoints, request/response formats, and usage examples.

## Contributing

Contributions are welcome! Please refer to the CONTRIBUTING.md file for guidelines.  

## License

This project is licensed under the MIT License.
