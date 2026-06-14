# Restoran — мобильное приложение владельца

Capacitor-оболочка для кабинета ресторана на [nohchi.net](https://nohchi.net).

- **Название:** Restoran
- **Bundle ID / Package:** `net.nohchi.restoran`
- **Версия:** 1.1

## Что внутри

Приложение открывает `https://nohchi.net/login/` в нативном WebView. Один код — две платформы: Android и iOS.

## Быстрый старт

```bash
git clone https://github.com/pikhaev1988/admin-app.git
cd admin-app
npm install
pip install -r scripts/requirements.txt   # для генерации иконок
```

---

## Android (Windows / Mac / Linux)

```bash
npm run build:apk
```

APK: `android/app/build/outputs/apk/debug/app-debug.apk`

Release:

```bash
npm run build:apk:release
```

---

## iOS (только Mac + Xcode)

### Требования

- macOS
- [Xcode](https://developer.apple.com/xcode/) 15+
- [CocoaPods](https://cocoapods.org/): `sudo gem install cocoapods`
- Apple Developer аккаунт ($99/год) — для TestFlight и App Store

### Сборка на Mac

```bash
npm run build:ios
cd ios/App
pod install
open App.xcworkspace
```

В Xcode:

1. Выберите **Team** (Signing & Capabilities)
2. Убедитесь, что Bundle Identifier = `net.nohchi.restoran`
3. Подключите iPhone или выберите симулятор
4. **Product → Run** (тест) или **Product → Archive** (публикация)

### TestFlight / App Store

1. **Product → Archive**
2. **Distribute App → App Store Connect**
3. После обработки — TestFlight для тестировщиков

---

## Сборка iOS без Mac (облако)

### Вариант A: GitHub Actions

При пуше в `main` запускается `.github/workflows/ios.yml` — проверяет, что проект собирается на симуляторе.

Для подписанного IPA и TestFlight используйте Codemagic (ниже) или добавьте секреты Apple в GitHub Actions.

### Вариант B: Codemagic (рекомендуется)

1. Зарегистрируйтесь на [codemagic.io](https://codemagic.io)
2. Подключите репозиторий `pikhaev1988/admin-app`
3. В **Teams → Code signing identities** загрузите сертификат и provisioning profile для `net.nohchi.restoran`
4. В **Integrations** подключите App Store Connect API key
5. Запустите workflow из `codemagic.yaml`

Codemagic соберёт `.ipa` и загрузит в TestFlight.

---

## Иконки

```bash
npm run build:icons
```

Генерирует иконки для Android (`android/app/src/main/res/`) и iOS (`ios/App/App/Assets.xcassets/AppIcon.appiconset/`).

---

## Структура проекта

```
admin-app/
├── www/                  # стартовая страница (редирект на nohchi.net)
├── android/              # Android Studio проект
├── ios/                  # Xcode проект
├── capacitor.config.json # конфиг Capacitor
├── codemagic.yaml        # облачная сборка iOS
└── scripts/
    └── generate_icons.py
```

## Полезные команды

| Команда | Описание |
|---------|----------|
| `npm run sync` | Синхронизировать web-код в Android и iOS |
| `npm run sync:ios` | Только iOS |
| `npm run open:ios` | Открыть Xcode |
| `npm run open:android` | Открыть Android Studio |

## PWA без App Store

На iPhone можно добавить сайт на экран: Safari → Поделиться → **На экран «Домой»**. Работает без Apple Developer, но без публикации в App Store.
