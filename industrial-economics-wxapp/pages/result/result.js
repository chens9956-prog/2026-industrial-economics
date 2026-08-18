const questions = require('../../data/questions.js');

Page({
  data: {
    record: null,
    checkCount: 0,
    countdownSeconds: 15,
    questions: questions,
    themeClass: 'theme-dark',
    themeName: '深色模式'
  },

  timer: null,

  onLoad(options) {
    if (options.record) {
      const record = JSON.parse(decodeURIComponent(options.record));
      const checkCount = parseInt(options.checkCount || 0);
      this.setData({ record, checkCount });

      if (checkCount > 0) {
        this.startCountdown();
      }
    }

    const savedTheme = wx.getStorageSync('theme_mode') || 'dark';
    this.applyTheme(savedTheme);
  },

  applyTheme(mode) {
    if (mode === 'light') {
      this.setData({ themeClass: 'theme-light', themeName: '浅色模式' });
    } else {
      this.setData({ themeClass: 'theme-dark', themeName: '深色模式' });
    }
  },

  onToggleTheme() {
    const current = wx.getStorageSync('theme_mode') === 'light' ? 'dark' : 'light';
    wx.setStorageSync('theme_mode', current);
    this.applyTheme(current);
  },

  onUnload() {
    if (this.timer) clearInterval(this.timer);
  },

  startCountdown() {
    this.timer = setInterval(() => {
      let sec = this.data.countdownSeconds - 1;
      if (sec <= 0) {
        clearInterval(this.timer);
        wx.navigateBack({ delta: 99 });
        return;
      }
      this.setData({ countdownSeconds: sec });
    }, 1000);
  },

  onBackHome() {
    if (this.timer) clearInterval(this.timer);
    wx.navigateBack({ delta: 99 });
  }
})
