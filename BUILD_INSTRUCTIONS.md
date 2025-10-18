# Building Battle Street Executables

This project uses GitHub Actions to automatically build executables for Windows and macOS.

## How to Use GitHub Actions

### Automatic Builds

The workflow automatically runs when you:
1. Push code to the `main` or `master` branch
2. Create a pull request to `main` or `master`

### Manual Builds

You can also trigger builds manually:

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. Select **Build Executables** workflow
4. Click **Run workflow**
5. Choose the branch and click **Run workflow**

## Downloading Built Executables

After a successful build:

1. Go to the **Actions** tab in your repository
2. Click on the most recent workflow run
3. Scroll down to **Artifacts**
4. Download the artifacts you need:
   - `BattleStreet-Windows` - Windows executable (.exe)
   - `BattleStreet-macOS` - macOS application bundle (.app)
   - `BattleStreet-All-Platforms` - Combined package with both versions

## Building Locally

If you want to build the executables locally instead of using GitHub Actions:

### Prerequisites
```bash
pip install pygame pyinstaller
```

### Windows
```bash
cd "Battle Street"
pyinstaller battle_street.spec --clean
```

The executable will be in `Battle Street/dist/BattleStreet.exe`

### macOS
```bash
cd "Battle Street"
pyinstaller battle_street.spec --clean
```

The app bundle will be in `Battle Street/dist/BattleStreet.app`

## Distribution

### Windows
- Distribute the `BattleStreet.exe` file
- Users can run it directly without installing Python or dependencies

### macOS
- Distribute the `BattleStreet.app` folder
- Users may need to right-click and select "Open" the first time (macOS security)
- For wider distribution, consider code signing the app

## Notes

- Built executables are stored for 30 days (Windows/macOS) or 90 days (combined)
- The workflow requires the `weapons/` folder to be included in the repository
- Save files (`battle_street_save.dat`) are created in the user's working directory

