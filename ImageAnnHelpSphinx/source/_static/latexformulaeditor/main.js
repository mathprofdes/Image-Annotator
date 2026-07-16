const {
  app,
  BrowserWindow
} = require('electron');

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1600,
    height: 1000,
    show: false
  });
  win.maximize();
  win.loadFile('index.html');

  win.once('ready-to-show', () => {
    win.show();
  });
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})