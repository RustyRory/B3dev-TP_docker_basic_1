import datetime
import platform
import os

def banner() -> str:
    name = os.getenv("WELCOME_NAME", "Docker")
    return (
        f"Bonjour {name} !\n"
        f"Date et heure : {datetime.datetime.utcnow().isoformat()}Z\n"
        f"Système : {platform.system()} {platform.release()}"
    )

if __name__ == "__main__":
    print(banner())
