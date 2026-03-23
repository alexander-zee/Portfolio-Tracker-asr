# =========================
# Imports
# =========================
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# MODEL
# =========================
@dataclass
class Asset:
    ticker: str
    sector: str
    asset_class: str
    quantity: float
    purchase_price: float

    @property
    def transaction_value(self) -> float:
        return self.quantity * self.purchase_price


class Portfolio:
    def __init__(self) -> None:
        self.assets: List[Asset] = []

    def add_asset(
        self,
        ticker: str,
        sector: str,
        asset_class: str,
        quantity: float,
        purchase_price: float
    ) -> None:
        asset = Asset(
            ticker=ticker.upper(),
            sector=sector,
            asset_class=asset_class,
            quantity=quantity,
            purchase_price=purchase_price
        )
        self.assets.append(asset)

    def get_assets(self) -> List[Asset]:
        return self.assets

    def compute_portfolio_table(self, current_prices: Dict[str, float]) -> pd.DataFrame:
        rows = []

        for asset in self.assets:
            current_price = current_prices.get(asset.ticker, np.nan)
            current_value = asset.quantity * current_price if not np.isnan(current_price) else np.nan

            rows.append({
                "Ticker": asset.ticker,
                "Sector": asset.sector,
                "Asset Class": asset.asset_class,
                "Quantity": asset.quantity,
                "Purchase Price": asset.purchase_price,
                "Transaction Value": asset.transaction_value,
                "Current Price": current_price,
                "Current Value": current_value
            })

        return pd.DataFrame(rows)

    def total_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        total = 0.0
        for asset in self.assets:
            if asset.ticker in current_prices:
                total += asset.quantity * current_prices[asset.ticker]
        return total

    def compute_weights(self, current_prices: Dict[str, float]) -> pd.DataFrame:
        df = self.compute_portfolio_table(current_prices)
        total_value = df["Current Value"].sum()

        if total_value > 0:
            df["Weight"] = df["Current Value"] / total_value
        else:
            df["Weight"] = np.nan

        return df[["Ticker", "Sector", "Asset Class", "Current Value", "Weight"]]

    def compute_group_weights(self, current_prices: Dict[str, float], group_col: str) -> pd.DataFrame:
        df = self.compute_portfolio_table(current_prices)
        grouped = df.groupby(group_col, as_index=False)["Current Value"].sum()
        total_value = grouped["Current Value"].sum()

        if total_value > 0:
            grouped["Weight"] = grouped["Current Value"] / total_value
        else:
            grouped["Weight"] = np.nan

        return grouped

    def tickers(self) -> List[str]:
        return sorted(list({asset.ticker for asset in self.assets}))


# =========================
# VIEW
# =========================
class PortfolioView:
    @staticmethod
    def show_message(message: str) -> None:
        print(message)

    @staticmethod
    def show_dataframe(df: pd.DataFrame, title: Optional[str] = None) -> None:
        if title:
            print(f"\n{title}")
            print("-" * len(title))
        if df.empty:
            print("No data available.")
        else:
            print(df.to_string(index=False))

    @staticmethod
    def plot_prices(price_df: pd.DataFrame, tickers: List[str]) -> None:
        plt.figure(figsize=(10, 6))
        for ticker in tickers:
            if ticker in price_df.columns:
                plt.plot(price_df.index, price_df[ticker], label=ticker)

        plt.title("Historical Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_simulation(simulated_paths: np.ndarray) -> None:
        plt.figure(figsize=(10, 6))
        plt.plot(simulated_paths[:, :100], alpha=0.4)  # only first 100 paths for readability
        plt.title("Monte Carlo Portfolio Simulation")
        plt.xlabel("Time Step")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# =========================
# CONTROLLER
# =========================
class PortfolioController:
    def __init__(self, portfolio: Portfolio, view: PortfolioView) -> None:
        self.portfolio = portfolio
        self.view = view

    def add_asset_interactive(self) -> None:
        ticker = input("Ticker: ").strip()
        sector = input("Sector: ").strip()
        asset_class = input("Asset class: ").strip()
        quantity = float(input("Quantity: ").strip())
        purchase_price = float(input("Purchase price: ").strip())

        self.portfolio.add_asset(ticker, sector, asset_class, quantity, purchase_price)
        self.view.show_message(f"Asset {ticker.upper()} added successfully.")

    def get_mock_current_prices(self) -> Dict[str, float]:
        prices = {}
        for ticker in self.portfolio.tickers():
            prices[ticker] = 100.0  # placeholder
        return prices

    def get_mock_historical_prices(self) -> pd.DataFrame:
        dates = pd.date_range(end=pd.Timestamp.today(), periods=252)
        data = {}

        rng = np.random.default_rng(42)
        for ticker in self.portfolio.tickers():
            returns = rng.normal(0.0003, 0.02, size=len(dates))
            prices = 100 * np.cumprod(1 + returns)
            data[ticker] = prices

        return pd.DataFrame(data, index=dates)

    def show_portfolio(self) -> None:
        current_prices = self.get_mock_current_prices()
        df = self.portfolio.compute_portfolio_table(current_prices)
        self.view.show_dataframe(df, "Current Portfolio")

    def show_weights(self) -> None:
        current_prices = self.get_mock_current_prices()

        asset_weights = self.portfolio.compute_weights(current_prices)
        sector_weights = self.portfolio.compute_group_weights(current_prices, "Sector")
        class_weights = self.portfolio.compute_group_weights(current_prices, "Asset Class")

        self.view.show_dataframe(asset_weights, "Asset Weights")
        self.view.show_dataframe(sector_weights, "Sector Weights")
        self.view.show_dataframe(class_weights, "Asset Class Weights")

    def show_prices(self) -> None:
        price_df = self.get_mock_historical_prices()
        tickers = self.portfolio.tickers()

        if not tickers:
            self.view.show_message("No assets in portfolio.")
            return

        self.view.show_dataframe(price_df.tail(), "Historical Price Snapshot")
        self.view.plot_prices(price_df, tickers)

    def run_simulation(self, years: int = 15, n_paths: int = 100_000) -> None:
        current_prices = self.get_mock_current_prices()
        initial_value = self.portfolio.total_portfolio_value(current_prices)

        if initial_value <= 0:
            self.view.show_message("Portfolio is empty or has zero value.")
            return

        steps = years * 12
        mu = 0.06
        sigma = 0.15
        dt = 1 / 12

        rng = np.random.default_rng(42)
        shocks = rng.normal(size=(steps, n_paths))

        paths = np.zeros((steps + 1, n_paths))
        paths[0] = initial_value

        for t in range(1, steps + 1):
            paths[t] = paths[t - 1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks[t - 1])

        self.view.show_message(f"Simulation completed with {n_paths:,} paths over {years} years.")
        self.view.plot_simulation(paths)

        percentiles = np.percentile(paths[-1], [5, 50, 95])
        summary = pd.DataFrame({
            "Percentile": ["5%", "50%", "95%"],
            "Terminal Value": percentiles
        })
        self.view.show_dataframe(summary, "Simulation Summary")

    def menu(self) -> None:
        while True:
            print("\nPortfolio Tracker")
            print("1. Add asset")
            print("2. Show portfolio")
            print("3. Show weights")
            print("4. Show prices")
            print("5. Run simulation")
            print("6. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_asset_interactive()
            elif choice == "2":
                self.show_portfolio()
            elif choice == "3":
                self.show_weights()
            elif choice == "4":
                self.show_prices()
            elif choice == "5":
                self.run_simulation()
            elif choice == "6":
                self.view.show_message("Exiting application.")
                break
            else:
                self.view.show_message("Invalid option. Please try again.")


# =========================
# MAIN
# =========================
def main() -> None:
    portfolio = Portfolio()
    view = PortfolioView()
    controller = PortfolioController(portfolio, view)
    controller.menu()


if __name__ == "__main__":
    main()