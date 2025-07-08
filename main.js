const { app, BrowserWindow } = require('electron');

function createWindow() {
    const win = new BrowserWindow({
        width: 400,
        height: 600,
        frame: false,          // ❌ removes title bar
        transparent: true,     // ✅ allows window transparency
        resizable: false,      
        alwaysOnTop: true,  
        hasShadow: false,      // optional: no window shadow
        webPreferences: {
          nodeIntegration: true,
          contextIsolation: false,
          backgroundThrottling: false,
        },
    });
        win.loadFile('index.html');
}

app.whenReady().then(createWindow);
