# Bro Django Administration
## Overview
This project is a Django site with its built-in user authentication system. This website log-in/sign-up page recieves and stores information about new users. This program goes through the following process...

### Sign Up
- The user fills a request form that GETS the users first name, last name, email, who reffered them, and their favorite sports team.
- It sends this information to the BRO email using a gmail server.
- If accepted, BRO will send an email with a randomized link to the sign up page.
- This collects the remaining information needed for a user (username and password).
- An email is sent to the user to confirm and activate the account.
- The user is now stored in the authentication system and they can now sign in with their credentials.

This is a project that demonstrates how it works and is the first building block to building social media sites, betting sites, etc.
