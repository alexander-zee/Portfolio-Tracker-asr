# Portfolio Tracker

## Description
This project is a command-line interface (CLI) application for tracking a simple investment portfolio. Users can add assets, view the current portfolio, analyze portfolio weights, retrieve historical prices, and run a Monte Carlo simulation to assess potential future portfolio performance. The application is structured around a Model-View-Controller (MVC) design using separate classes for the portfolio logic, presentation layer, and user interaction flow.

## Features
- Add assets by specifying ticker, sector, asset class, quantity, and purchase price
- View the current portfolio with transaction value, current price, and current value
- Compute portfolio weights by asset, sector, and asset class
- View profit and loss per asset
- Retrieve historical prices using Yahoo Finance
- Plot historical prices and normalized price performance
- Run a 15-year Monte Carlo simulation with 100,000 paths
- Load a demo portfolio for quick testing

## Project Structure
Although the project is implemented in a single script, it follows an MVC-style structure:
- Model: Asset and Portfolio
- View: PortfolioView
- Controller: PortfolioController

## Installation
Clone the repository and install the required dependencies:

pip install -r requirements.txt

## Requirements
This project uses:
- Python
- NumPy
- pandas
- matplotlib
- yfinance

## Usage
Run the application from the command line:

python main.py

After starting the program, the following menu is shown:
1. Add asset
2. Show portfolio
3. Show weights
4. Show prices and charts
5. Run 15-year simulation
6. Show profit/loss
7. Load demo portfolio
8. Exit

## Example Workflow
A typical workflow is:
1. Load the demo portfolio or add assets manually
2. Show the current portfolio
3. Inspect asset, sector, and asset class weights
4. View historical price charts
5. Run the Monte Carlo simulation to analyze possible future portfolio values

## Simulation Approach
The simulation is based on historical log returns of the portfolio assets. Expected annual returns and the covariance structure are estimated from historical price data. These are then used to derive the portfolio’s expected return and volatility. Future portfolio values are simulated monthly over a 15-year horizon using a Geometric Brownian Motion framework with 100,000 simulated paths. The application reports summary statistics such as mean terminal value, median terminal value, and percentile outcomes, and plots a subset of the simulated paths.

## Notes
- Historical and current price data are retrieved through Yahoo Finance via the yfinance package
- If ticker data cannot be retrieved, the application handles this by showing missing values where relevant
- The demo portfolio contains AAPL, MSFT, JNJ, and XOM for quick testing
