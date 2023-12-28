# Price Tracker Project

## Introduction

This repository contains a Python project focused on web scraping product prices of specific brands from an online shopping site. The scraped data, including changing prices over time, is stored in MongoDB Cloud. The primary objective is to regularly update product prices for specific brands and track changes on the user-facing website.

## Project Details

### Used Libraries and Technologies

- Python
- BeautifulSoup (for web scraping)
- Requests (for fetching web pages)
- Pandas (for data processing and manipulation)
- MongoDB (as the database)
- MongoDB Atlas (for cloud-based database usage)

### Web Scraping and Data Extraction

- Web scraping was performed using the `requests` and `BeautifulSoup` libraries to extract product names and prices for specific brands from the online shopping site.
- The extracted data was processed and transformed into a Pandas DataFrame.

### Changing Prices Over Time and Data Processing

- Matching the extracted data with the current timestamp was done to identify changing prices over time.
- Price information was formatted appropriately, and data was processed before being saved to the database.

### MongoDB Cloud Database and Data Storage

- Setting up a MongoDB Atlas cloud-based database.
- Establishing a connection between Python and MongoDB Atlas using the `pymongo` library.
- Storing the processed data in the MongoDB database.

## Additional Note

This project is automatically executed daily using Google Cloud Function and Google Cloud Scheduler.
It fetches data and stores it in MongoDB Atlas for approximately 40 days. The automation ensures that the product prices are regularly
updated and tracked seamlessly in the cloud environment.
