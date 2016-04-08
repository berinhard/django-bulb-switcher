Django Bulb Switcher: DB Independent Feature Toggle Tool
========================================================
========================================================

*Django Bulb Switcher* offers you a way to configure conditions and associate these conditions to permission flags.

Install
=======

.. code-block:: console

    pip install git+ssh://git@github.com/berinhard/django-bulb-switcher.git@0.1#egg=django_bulb_switcher


Usage and Info
==============

Django Bulb Switcher is divided just on configuration and checking which flags were turned on/off by request.

Step 1: Setting up the middleware
---------------------------------

Adds to your middleware classes:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        ....
        'django_bulb_switcher.middlewares.ContionalBulbSwitcherMiddleware',
    ]

Step 2: Config the conditionals dict
------------------------------------

The conditionals dict is composed of a list of callable objects. Each one of them must return True or False and the flag will be active on the request if *all* of them return True for the pair of parameters request and user. Here is an exemple of a conditional:

.. code-block:: python

    def staff_condition(request, user):
        return user.is_staff

    def superuser_condition(request, user):
        return user.is_superuser

And at your settings.py:

.. code-block:: python

    from your_app.conditionals import staff_condition, superuser_condition

    BULB_SWITCHER_CONDITIONALS = {
        'access_to_master_admin_page': [staff_condition, superuser_condition],
        'partial_access_to_admin_page': [staff_condition],
    }

You could also define your conditionals without importing them as follows:

.. code-block:: python

    BULB_SWITCHER_CONDITIONALS = {
        'access_to_master_admin_page': ['your_app.conditionals.staff_condition', 'your_app.conditionals.superuser_condition'],
        'partial_access_to_admin_page': ['your_app.conditionals.staff_condition'],
    }


Step 3: Checking the flag status
--------------------------------

Now you can check and decide how you'll process your view just like the following example:

.. code-block:: python

    from django_bulb_switcher import bulb_checker

    def your_view_request(request):
        admin_flag, partial_flag = 'access_to_master_admin_page', 'partial_access_to_admin_page'
        if bulb_checker.is_off(request, admin_flag) and bulb_checker.is_off(request, partial_flag):
            # None of the flags are actives flow
        elif bulb_checker.is_on(request, admin_flag):
            # admin flow
        elif bulb_checker.is_on(request, partial_flag):
            # commom staff flow
