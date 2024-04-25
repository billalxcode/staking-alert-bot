import os
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from eth_utils.currency import from_wei, to_wei
from datetime import timedelta
from coinmarketcapapi import CoinMarketCapAPI

group_id = -1002099408316
# group_id = -4112324237
cmc = CoinMarketCapAPI(api_key="165526c2-ae2f-4e24-8fb4-1cfa4390ef58")
bot = Bot("7134780818:AAEu_iDWNB4c5uPPrKk0nCenz4aD2QU3qwQ")
animation = os.path.join(
    os.getcwd(),
    "assets",
    "video.mp4"
)

async def startDepositBroadcast(stakeAmount: str, duration: timedelta, apy: str, totalStaked: str, tx: str):
    print ("Staring broadcast")
    
    stakeAmountConverted = from_wei(stakeAmount, 'gwei')
    totalStakedConverted = from_wei(totalStaked, 'gwei')

    stakePriceResponse            = cmc.tools_priceconversion(symbol="PIA", amount=stakeAmountConverted)
    totalStakedPriceResponse      = cmc.tools_priceconversion(symbol="PIA", amount=totalStakedConverted)

    if stakePriceResponse.ok:
        stakePrice = round(stakePriceResponse.data[0]['quote']['USD']['price'], 5)
    else:
        stakePrice = "0"
    if totalStakedPriceResponse.ok:
        totalStakedPrice = round(totalStakedPriceResponse.data[0]['quote']['USD']['price'], 5)
    else:
        totalStakedPrice = "0"
    keyboard = [
        [
            InlineKeyboardButton("STAKE $PIA HERE", 'https://stake.olympiaai.io')
        ],
        [
            InlineKeyboardButton('TX HHASH', f"https://etherscan.io/tx/{tx}")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    text = f"""
NEW $PIA STAKE!
            
🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠
            
🤖 Amount Staked
{round(stakeAmountConverted, 3)} $PIA | ${stakePrice}
        
⏰ Duration
{duration.days} days | {apy}% APY
        
🔒 Total Staked
{round(totalStakedConverted, 5)} $PIA | ${totalStakedPrice}
    """
    await bot.send_animation(
        chat_id=group_id,
        animation=open(animation, "rb"),
        caption=text,
        reply_markup=markup
    )

async def startWithdrawBroadcast(amountWithdrawn: str, duration: timedelta, apy: str, totalStaked: str, tx: str):
    print ("Staring broadcast")
    
    amountWithdrawnConverted = from_wei(amountWithdrawn, 'gwei')
    totalStakedConverted = from_wei(totalStaked, 'gwei')

    keyboard = [
        [
            InlineKeyboardButton("STAKE $PIA HERE", 'https://stake.olympiaai.io')
        ],
        [
            InlineKeyboardButton('TX HHASH', "https://google.com")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    text = f"""
NEW $PIA WITHDRAWAL!
            
🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠
            
🤖 Amount Withdrawn
{round(amountWithdrawnConverted, 3)} $PIA
        
⏰ Duration
{duration.days} days | {apy}% APY
        
🔒 Total Staked
{round(totalStakedConverted, 3)}
    """
    await bot.send_message(
        chat_id=group_id,
        text=text,
        reply_markup=markup
    )

async def startEmergencyWithdrawBroadcast(amountWithdrawn: str, duration: timedelta, apy: str, totalStaked: str, tx: str):
    print ("Staring broadcast")
    
    amountWithdrawnConverted = from_wei(amountWithdrawn, 'gwei')
    totalStakedConverted = from_wei(totalStaked, 'gwei')

    keyboard = [
        [
            InlineKeyboardButton("STAKE $PIA HERE", 'https://stake.olympiaai.io')
        ],
        [
            InlineKeyboardButton('TX HHASH', "https://google.com")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    text = f"""
NEW $PIA EMERGENCY WITHDRAWAL!
            
🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠
            
🤖 Amount Withdrawn
{amountWithdrawnConverted} $PIA
        
⏰ Duration
{duration.days} days | {apy}% APY
        
🔒 Total Staked
{totalStakedConverted}
    """
    await bot.send_message(
        chat_id=group_id,
        text=text,
        reply_markup=markup
    )
