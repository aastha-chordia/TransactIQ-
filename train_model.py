from app.services import train_if_missing, get_model
if __name__ == "__main__":
    train_if_missing()
    model = get_model()
    print("TransactIQ Random Forest model trained and saved.")
    print(f"Features: {model.n_features_in_}")
