# Django Restaurant Management System

A robust Restaurant Management System built with Django. This project facilitates the management of restaurant operations including menu creation, table management, order processing, kitchen display system, billing, inventory management, staff management, and user authentication.

## Features

-Comming Soon

## Project Structure

<pre><code>

Comming Soon
      
</code></pre>

## Getting Started

### Prerequisites

- Python 3.6+
- Django 3.2+
- Git

### Installation

1. Install Python
2. Install Django
   <pre><code>
   pip install django
   </code></pre>
3. Install Django PhoneNumberField
   <pre><code>
   pip install django-phonenumber-field
   </code></pre>
4. Install num2words
   <pre><code>
   pip install num2words
   </code></pre>   
5. Install Virtual Environment
   <pre><code>
   pip install virtualenv
   </code></pre>
6. Clone the repository
   <pre><code>
   git clone https://github.com/pokharelsugam/rms-django.git
   cd rms-django
   </code></pre>
7. Create a virtual environment and activate it.
   <pre><code>
   virtualenv env
   env\scripts\activate
   pip install django
   pip install django-phonenumber-field
   pip install num2words
   </code></pre>
8. Run the migrations
    <pre><code>
    python manage.py makemigrations #may or may not be required
    python manage.py migrate	#must be required
    </code></pre>
9. Create a superuser
    <pre><code>
    python manage.py createsuperuser
    </code></pre>
	### While creating superuser phone number must write in international format like +[country_code][phone_number] e.g.; +9779812345678
10. Start the development server
    <pre><code>
    python manage.py runserver
    </code></pre>

## Usage
<ul>
<li>Navigate to http://127.0.0.1:8000/admin to access the admin interface and manage your restaurant data.</li>
<li>Create staff from registration form.</li>
<li>If if you need to assign superuser to staff please go django admin pannel through http://127.0.0.1:8000/admin/staff/staff/ and navigate to staff.</li>
</ul>
