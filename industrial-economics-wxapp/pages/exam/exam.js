const questions = require('../../data/questions.js');

Page({
  data: {
    student: { id: '', name: '' },
    questions: questions,
    userAnswers: {},
    selectedMap: {},
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
    const { qid, type, key } = e.currentTarget.dataset;
    let userAnswers = { ...this.data.userAnswers };
    let selectedMap = { ...this.data.selectedMap };

    if (type === 'single') {
      userAnswers[qid] = key;
    } else {
      // Multiple choice toggle
      const mapKey = qid + '_' + key;
      selectedMap[mapKey] = !selectedMap[mapKey];

      let currentKeys = [];
      ['A', 'B', 'C', 'D'].forEach(k => {
        if (selectedMap[qid + '_' + k]) currentKeys.push(k);
      });

      if (currentKeys.length > 0) {
        userAnswers[qid] = currentKeys.join('');
      } else {
        delete userAnswers[qid];
      }
    }

    const answeredCount = Object.keys(userAnswers).length;
    this.setData({ userAnswers, selectedMap, answeredCount });
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

    let totalScore = 0;
    let correctCount = 0;

    this.data.questions.forEach(q => {
      const uAns = this.data.userAnswers[q.id] || '';
      const cAns = q.answer;

      if (q.type === 'single') {
        if (uAns === cAns) {
          totalScore += 1.5;
          correctCount++;
        }
      } else {
        if (uAns.split('').sort().join('') === cAns.split('').sort().join('')) {
          totalScore += 2.0;
          correctCount++;
        }
      }
    });

    totalScore = Math.round(totalScore * 10) / 10;
    const accuracy = Math.round((correctCount / this.data.questions.length) * 100) + '%';
    const durationMin = Math.floor(this.timeElapsed / 60);
    const durationSec = this.timeElapsed % 60;
    const duration = `${String(durationMin).padStart(2, '0')}:${String(durationSec).padStart(2, '0')}`;

    const record = {
      id: this.data.student.id,
      name: this.data.student.name,
      score: totalScore,
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
