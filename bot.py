from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = "8703775657:AAH87ae1I9BE_8txMtkY8Q6ma0x9qhwzCfA"

# 💰 SOLDE (juste toi)
soldes = {
    5202457776: 5
}

attente_screen = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    solde = soldes.get(user_id, 0)

    clavier = [
        [InlineKeyboardButton("🛍️ Boutique", callback_data="boutique")],
        [InlineKeyboardButton("💳 Déposer", callback_data="deposer")],
        [InlineKeyboardButton("📢 Canal", url="https://t.me/zzcclbx")]
    ]

    await update.message.reply_text(
        f"""🎉 Bienvenue !

👤 {update.effective_user.first_name}
🆔 {user_id}
💰 Solde : {solde}€
🆘 pour toute question contactez le support @uhq95z

Choisissez une option 👇 """,
        reply_markup=InlineKeyboardMarkup(clavier)
    )


# BOUTONS
async def boutons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # BOUTIQUE
    if query.data == "boutique":

        await query.edit_message_text(
            "🛍️ Boutique\n\nChoisissez une offre :",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🥉 Classic 40€ -> ~200-500€", callback_data="classic")],
                [InlineKeyboardButton("🏅 Gold 100€ -> ~1500€", callback_data="gold")],
                [InlineKeyboardButton("👑 Premium 200€ -> ~3500€", callback_data="premium")],
                [InlineKeyboardButton("⬅️ Retour", callback_data="retour")]
            ])
        )

    elif query.data == "classic":

        await query.edit_message_text(
            "🥉 Classic\n💰 40€",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Payer", callback_data="pay_classic")],
                [InlineKeyboardButton("⬅️ Retour", callback_data="boutique")]
            ])
        )

    elif query.data == "gold":

        await query.edit_message_text(
            "🏅 Gold\n💰 100€",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Payer", callback_data="pay_gold")],
                [InlineKeyboardButton("⬅️ Retour", callback_data="boutique")]
            ])
        )

    elif query.data == "premium":

        await query.edit_message_text(
            "👑 Premium\n💰 200€",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Payer", callback_data="pay_premium")],
                [InlineKeyboardButton("⬅️ Retour", callback_data="boutique")]
            ])
        )

    # PAYMENTS
    elif query.data in ["pay_classic", "pay_gold", "pay_premium"]:

        prix = {
            "pay_classic": 40,
            "pay_gold": 100,
            "pay_premium": 200
        }

        nom = {
            "pay_classic": "CC Classic",
            "pay_gold": "CC Gold",
            "pay_premium": "CC Premium"
        }

        solde = soldes.get(user_id, 0)

        if solde >= prix[query.data]:

            soldes[user_id] -= prix[query.data]

            await query.edit_message_text(
                f"🛍️ Merci pour votre achat ! 🛍️\n\n{nom[query.data]}"
            )

        else:

            await query.edit_message_text(
                "❌ Solde insuffisant",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Retour", callback_data="retour")]
                ])
            )

    # RETOUR
    elif query.data == "retour":

        await query.edit_message_text(
            "🎉 Menu principal",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛍️ Boutique", callback_data="boutique"),
                 InlineKeyboardButton("💳 Déposer", callback_data="deposer")]
            ])
        )

    # DEPOT
    elif query.data == "deposer":

        solde = soldes.get(user_id, 0)

        await query.edit_message_text(
            f"💰 DÉPÔT\n\nSolde : {solde}€",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("40€", callback_data="dep_40"),
                 InlineKeyboardButton("60€", callback_data="dep_60")],
                [InlineKeyboardButton("100€", callback_data="dep_100"),
                 InlineKeyboardButton("200€", callback_data="dep_200")],
                [InlineKeyboardButton("⬅️ Retour", callback_data="retour")]
            ])
        )

    # DEPOT STEP 2
    elif query.data.startswith("dep_"):

        montant = query.data.split("_")[1]

        await query.edit_message_text(
            f"💳 Montant : {montant}€\n\nChoisissez méthode :",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Paypal", callback_data=f"paypal_{montant}")],
                [InlineKeyboardButton("Solana", callback_data=f"solana_{montant}")],
                [InlineKeyboardButton("Bitcoin", callback_data=f"btc_{montant}")],
                [InlineKeyboardButton("⬅️ Retour", callback_data="deposer")]
            ])
        )

    # PAYPAL
    elif query.data.startswith("paypal_"):

        montant = query.data.split("_")[1]

        await query.edit_message_text(
            text=(
                f"💰 ENVOYEZ EXACTEMENT {montant}€\n\n"
                "💳 Moyen de paiement : Paypal\n\n"
                "📌 A RENTRER DANS PAYPAL : @ladallelacc \n\n"
                "📸 Une fois payé, envoyez un screen ici."
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour menu", callback_data="retour")]
            ])
        )

    # SOLANA
    elif query.data.startswith("solana_"):

        montant = query.data.split("_")[1]

        await query.edit_message_text(
            text=(
                f"💰 ENVOYEZ EXACTEMENT {montant}€\n\n"
                "💳 Moyen de paiement : Solana\n\n"
                "📸 Une fois payé, envoyez un screen ici.\n\n"
                "📌 ADRESSE : HxhJXnKVTwjKn4bsMjH9JFJ5A65xSYgS59BbvnHRgq9e"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour menu", callback_data="retour")]
            ])
        )

    # BTC
    elif query.data.startswith("btc_"):

        montant = query.data.split("_")[1]

        await query.edit_message_text(
            text=(
                f"💰 ENVOYEZ EXACTEMENT {montant}€\n\n"
                "💳 Moyen de paiement : Bitcoin\n\n"
                "📸 Une fois payé, envoyez un screen ici.\n\n"
                "📌 ADRESSE 14BzJbDmHKgwW6qgnBcKRsyQtzD7idqyPF"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour menu", callback_data="retour")]
            ])
        )


# PHOTO
async def photo_recue(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if attente_screen.get(user_id):

        attente_screen.pop(user_id, None)

        await update.message.reply_text(
            "📸 Merci pour ta commande !\nLe staff validera au plus vite ton solde."
        )


# BOT
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(boutons))
app.add_handler(MessageHandler(filters.PHOTO, photo_recue))

print("Bot lancé...")

app.run_polling()
