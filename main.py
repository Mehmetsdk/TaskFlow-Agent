import sys

from src.agent import TaskAgent


def main() -> None:
    print("=" * 60)
    print("🤖 AI Agentic Engineer - Task Execution Agent'a Hoş Geldiniz!")
    print("Çıkmak için: 'q', 'quit' veya 'exit' yazabilirsiniz.")
    print("=" * 60)

    try:
        agent = TaskAgent()
    except Exception as exc:
        print(f"\n❌ BAŞLATMA HATASI: {exc}")
        print("Lütfen .env dosyanızda geçerli bir GEMINI_API_KEY (veya GOOGLE_API_KEY) olduğundan emin olun.")
        sys.exit(1)

    while True:
        try:
            user_input = input("\nSen: ")
            if user_input.lower() in ["q", "quit", "exit"]:
                print("\nGörüşmek üzere!")
                break

            if not user_input.strip():
                continue

            print("\n🤖 Agent düşünüyor (ve gerekirse araçları kullanıyor)...\n")
            response = agent.process_input(user_input)
            print(f"🤖 Agent:\n{response}")

        except KeyboardInterrupt:
            print("\n\nÇıkış yapılıyor...")
            break
        except Exception as exc:
            print(f"\n❌ Bir çalışma hatası oluştu: {exc}")

if __name__ == "__main__":
    main()
