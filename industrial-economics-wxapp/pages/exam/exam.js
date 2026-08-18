const questions = require('../../data/questions.js');

Page({
  data: {
    student: { id: '', name: '' },
    questions: questions,
    userAnswers: {},
    answeredCount: 0,
    timeRemaining: 75 * 60,
    timerStr: '75:00',
    themeClass: 'theme-dark',
    themeName: '深色模式'
  },

  timerInterval: null,
  timeElapsed: 0,

  onLoad() {
    const student = getApp().globalData.currentStudent || { id: '2026010001', name: '高建刚' };
    this.setData({ student });
    this.startTimer();

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
    if (this.timerInterval) clearInterval(this.timerInterval);
  },

  startTimer() {
    this.updateTimerStr();
    this.timerInterval = setInterval(() => {
      let timeRemaining = this.data.timeRemaining - 1;
      this.timeElapsed += 1;

      if (timeRemaining <= 0) {
        clearInterval(this.timerInterval);
        wx.showModal({
          title: '考试时间到',
          content: '75分钟倒计时结束，系统已为您自动交卷！',
          showCancel: false,
          success: () => this.submitExam()
        });
        return;
      }

      this.setData({ timeRemaining });
      this.updateTimerStr();
    }, 1000);
  },

  updateTimerStr() {
    const mins = Math.floor(this.data.timeRemaining / 60);
    const secs = this.data.timeRemaining % 60;
    const timerStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    this.setData({ timerStr });
  },

  onSelectOption(e) {
    const { qid, key } = e.currentTarget.dataset;
    const userAnswers = { ...this.data.userAnswers, [qid]: key };
    const answeredCount = Object.keys(userAnswers).length;
    this.setData({ userAnswers, answeredCount });
  },

  onExitExam() {
    wx.showModal({
      title: '退出考试确认',
      content: '确定要退出本次随堂考试吗？未提交的选项将被清空，您可稍后再重新登录作答。',
      success: (res) => {
        if (res.confirm) {
          if (this.timerInterval) clearInterval(this.timerInterval);
          wx.navigateBack();
        }
      }
    });
  },

  onSubmitExam() {
    const unanswered = this.data.questions.length - this.data.answeredCount;
    if (unanswered > 0) {
      wx.showModal({
        title: '交卷确认',
        content: `您还有 ${unanswered} 道题未作答，确定要现在交卷吗？`,
        success: (res) => {
          if (res.confirm) this.submitExam();
        }
      });
    } else {
      this.submitExam();
    }
  },

  submitExam() {
    if (this.timerInterval) clearInterval(this.timerInterval);

    let correctCount = 0;
    this.data.questions.forEach(q => {
      if (this.data.userAnswers[q.id] === q.answer) correctCount++;
    });

    const score = correctCount * 2;
    const accuracy = Math.round((correctCount / this.data.questions.length) * 100) + '%';
    const durationMin = Math.floor(this.timeElapsed / 60);
    const durationSec = this.timeElapsed % 60;
    const duration = `${String(durationMin).padStart(2, '0')}:${String(durationSec).padStart(2, '0')}`;

    const record = {
      id: this.data.student.id,
      name: this.data.student.name,
      score,
      accuracy,
      duration,
      userAnswers: this.data.userAnswers,
      scoreCheckedCount: 0,
      timestamp: new Date().toLocaleString('zh-CN', { hour12: false })
    };

    let submissions = wx.getStorageSync('exam_submissions_v1') || [];
    let idx = submissions.findIndex(r => r.id.trim() === record.id.trim());
    if (idx >= 0) submissions[idx] = record;
    else submissions.unshift(record);
    wx.setStorageSync('exam_submissions_v1', submissions);

    wx.redirectTo({
      url: `/pages/result/result?record=${encodeURIComponent(JSON.stringify(record))}&checkCount=0`
    });
  }
})
