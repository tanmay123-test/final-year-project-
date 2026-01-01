import requests

API = "http://127.0.0.1:5000"
TOKEN = None


# ---------------- USER SIGNUP WITH EMAIL OTP ----------------
def signup():
    print("\n👤 User Signup (Email OTP)")
    name = input("Name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    email = input("Email: ").strip()

    # Step 1: Create user (unverified)
    r = requests.post(
        f"{API}/signup",
        json={
            "name": name,
            "username": username,
            "password": password,
            "email": email
        }
    )

    if r.status_code != 201:
        print("❌ Signup failed:", r.json())
        return

    print(f"📨 OTP sent to {email}")

    # Step 2: OTP verification loop (max 3 tries handled by backend)
    while True:
        print("\n1. Enter OTP")
        print("2. Resend OTP")
        print("3. Cancel signup")

        choice = input("Choice: ").strip()

        if choice == "1":
            otp = input("Enter OTP from email: ").strip()

            r = requests.post(
                f"{API}/verify-otp",
                json={
                    "email": email,
                    "otp": otp
                }
            )

            if r.status_code == 200:
                print("✅ Account verified successfully")
                return
            else:
                print("❌", r.json().get("error", "OTP verification failed"))

        elif choice == "2":
            r = requests.post(
                f"{API}/resend-otp",
                json={"email": email}
            )

            if r.status_code == 200:
                print("📨 OTP resent successfully")
            else:
                print("❌ Failed to resend OTP")

        elif choice == "3":
            print("❌ Signup cancelled")
            return

        else:
            print("❌ Invalid choice")


# ---------------- LOGIN ----------------
def login():
    global TOKEN
    print("\n🔐 Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    r = requests.post(
        f"{API}/login",
        json={
            "username": username,
            "password": password
        }
    )

    if r.status_code == 200:
        TOKEN = r.json()["token"]
        print("✅ Logged in successfully")
    else:
        print("❌ Login failed:", r.json().get("error"))


# ---------------- PROTECTED QUERY ----------------
def ask():
    if not TOKEN:
        print("⚠️ Please login first")
        return

    query = input("Ask ExpertEase: ").strip()

    r = requests.post(
        f"{API}/expert-query",
        json={"query": query},
        headers={"Authorization": TOKEN}
    )

    print(r.json())


# ---------------- MAIN MENU ----------------
def main():
    while True:
        print("\n--- ExpertEase ---")
        print("1. User Signup (Email OTP)")
        print("2. Login")
        print("3. Ask Expert")
        print("4. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            ask()
        elif choice == "4":
            print("👋 Goodbye")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
