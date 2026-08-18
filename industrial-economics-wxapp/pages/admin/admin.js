Page({
  data: {
    isUnlocked: false,
    passVal: '',
    passError: false,
    activeTab: 'scores',
    records: [],
    rosterText: ''
  },

  onInputPass(e) {
    this.setData({ passVal: e.detail.value.trim() });
  },

  onAdminLogin() {
    if (this.data.passVal === 'admin126') {
      this.setData({ isUnlocked: true, passError: false });
      this.loadData();
    } else {
      this.setData({ passError: true });
    }
  },

  loadData() {
    const records = wx.getStorageSync('exam_submissions_v1') || [];
    let roster = wx.getStorageSync('student_roster_v1') || [
      { id: '2026010001', name: '高建刚' },
      { id: '2026010002', name: '李明' },
      { id: '2026010003', name: '王芳' }
    ];
    const newlineChar = String.fromCharCode(10);
    const rosterText = roster.map(s => s.id + ',' + s.name).join(newlineChar);
    this.setData({ records, rosterText });
  },

  onSwitchTab(e) {
    this.setData({ activeTab: e.currentTarget.dataset.tab });
  },

  onInputRosterText(e) {
    this.setData({ rosterText: e.detail.value });
  },

  onSaveRoster() {
    const newlineChar = String.fromCharCode(10);
    const lines = this.data.rosterText.split(newlineChar);
    const newRoster = [];
    lines.forEach(l => {
      const parts = l.split(/[,，\s]+/).filter(Boolean);
      if (parts.length >= 2) newRoster.push({ id: parts[0], name: parts[1] });
    });
    if (newRoster.length === 0) {
      wx.showToast({ title: '格式有误', icon: 'none' });
      return;
    }
    wx.setStorageSync('student_roster_v1', newRoster);
    wx.showToast({ title: `成功保存 ${newRoster.length} 名学生`, icon: 'success' });
  },

  onClearRecords() {
    wx.showModal({
      title: '清空确认',
      content: '确定要清空所有已保存的学生成绩记录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('exam_submissions_v1');
          this.setData({ records: [] });
        }
      }
    });
  }
})
