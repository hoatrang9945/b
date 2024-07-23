<h1 align="center"> SOLANA BOT </h1> <br>
<p align="center">
  <a href=""> 
     
  </a>
</p>

<p align="center">
  A Bot in your pocket based on take profit or buy/sell on Raydium.
</p>
<center> <img width="877" alt="1" src="https://github.com/user-attachments/assets/3738dec1-c995-4fda-b66c-935d6043727c"> </center>


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#Usage)
- [Setting](#Setting-)
- [Disclaimer ](#Disclaimer)
- [Contact ](#Contact)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

The Solana Sniper/Trading Bot is a groundbreaking tool in the booming Solana ecosystem, designed to tackle a common issue faced by traders: missing out on profit opportunities after purchasing tokens on the Solana network, leading to token rug-pulls or dumps. This software not only integrates sniping functionality, allowing users to instantly acquire tokens upon their launch but also adds trading tools to optimize one’s position.

**Available for both iOS and Android and PC .**
![Screenshot 2024-04-05 052559](https://github.com/olymporod/Solana-Snipe-Bot/assets/166156731/85f5eee8-dfdb-4a13-b7c0-dd0876e91d2d)



<p align="center">
  <a href ="https://t.me/OlympusHenry">
  
  </a>
</p>

## Features

A few of the things you can do with Bot:

- Sniping: Execute buy transactions instantly when liquidity is added to an SPL token, ensuring you're among the first to buy in promising new tokens.
- Take Profit: Automatically sell tokens at a predefined profit percentage, securing gains.
- Buy/Sell x Times: Execute repeated buy orders to average down or scale into positions.
- Sell Limit Order: Set your tokens to sell automatically at a predetermined price, locking in profits.
- User friendly interface - hands-on interface

**Making the first to trade in new tokens.**
<img width="910" alt="2" src="https://github.com/user-attachments/assets/a85bd1f2-c152-42a3-8b27-c3bb31cb59e2">


## Installation

- Downloads Python ( Recommend the latest version )  [Python 3.12.4](https://www.python.org/downloads/)
-  ***VERY IMPORTANT***: When installing Python also install **"Add python.exe to path"** and ***"Use admin privileges when installing py.exe:*** => Tick 

## Usage

- Update `pip` Run the following command to update pip to the latest version

```python
python -m pip install --upgrade pip
```
- Clone or download the project

```git 
git clone https://github.com/fsolanathon/SOLANA-SNIPER-BOT.git
```

Option 2: Download the project directly

Go to the project's GitHub page, click the "Code" button and select "Download ZIP". Unzip the downloaded ZIP file to get the project folder.

- Navigate to the project folder

Open a terminal and navigate to the project folder

```python
cd SOLANA-SNIPER-BOT
```

- Install libraries

Run the following command to install the required libraries for the project:

```python
pip install -r requirements.txt
```

- Run the project

Run the following command to start the project:



```python
python main.py
```



## Setting

- **BUY DELAY** : In seconds after launch. Set to 0, Token will buy immediately after token launch
- **TAKE PROFIT** : Take-Profit Order (TP) . Token places a sell order and confirms immediately after reaching the target
- **STOP LOSS** : Percentage loss at which to stop the loss.
- **SELL DELAY** : to the number of seconds you want to wait before selling the token. Set to 0, token will be sold immediately after it is bought.
- **BUY/SELL RETRIES** : Maximum number of retries for buying/selling a token.
- **BUY/SELL SLIPPAGE** : Slippage %.
- **CHECK BURNED** : Set to true to buy tokens only if their liquidity pool is burned.
- **CHECK RENOUNCED** : Set to true to buy tokens only if their mint is renounced.
- **CHECK RUG** : Set to true to check the risk score and protect against rug pulls.





# Contact
[Telegram](https://t.me/SAthonSolana)
- Telegram : @SAthonSolana


## Disclaimer

- This extension is not affiliated with Solana Foundation or Solana Labs. It is a non-profit community project.
- Solana Snipe is in active development, so all the snippets are subject to change.
- The snippets are unaudited. Use at your own risk.
