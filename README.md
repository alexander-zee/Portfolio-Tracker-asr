# Portfolio Tracker

## Description

This project is a command-line interface (CLI) application to track and simulate an investment portfolio. It allows users to manage assets, analyze portfolio composition, and simulate future portfolio performance using Monte Carlo methods.

## Features

* Add assets (ticker, sector, asset class, quantity, purchase price)
* View current portfolio value
* Compute asset, sector, and asset class weights
* Retrieve and plot historical price data
* Run Monte Carlo simulations (15 years, 100,000 paths)
* Analyze profit and loss per asset

## Installation

Install the required dependencies:

pip install -r requirements.txt

## Usage

Run the application:

python main.py

Then follow the CLI menu to interact with the portfolio.

## Example

* Load demo portfolio
* View portfolio and weights
* Run simulation to analyze future performance

## Design

The project follows a Model-View-Controller (MVC) architecture:

* Model: portfolio data and financial calculations
* View: CLI interface and visualizations
* Controller: handles user interaction and program flow

## Technologies

* Python
* NumPy
* Pandas
* Matplotlib
* yfinance
