import os

base_dir = r'l:\我的云端硬盘\2026产业经济学\glass-calculator-wxapp'

# 1. Update index.wxml to feature "⌫ 撤销" button
index_wxml = """<view class="container {{skinMode}}">

  <!-- CUTE ANIMAL DECORATION -->
  <view class="cute-ears-wrapper" wx:if="{{skinMode === 'skin-penguin'}}">
    <view class="penguin-ear left-ear"><view class="inner-ear"></view></view>
    <view class="penguin-beak">🐧</view>
    <view class="penguin-ear right-ear"><view class="inner-ear"></view></view>
  </view>

  <view class="cute-ears-wrapper" wx:if="{{skinMode === 'skin-bear'}}">
    <view class="bear-ear left-ear"></view>
    <view class="bear-face">🐻</view>
    <view class="bear-ear right-ear"></view>
  </view>

  <!-- CALCULATOR MAIN CARD -->
  <view class="calc-card">

    <!-- Skin Switcher Header Controls -->
    <view class="calc-header">
      <view class="title-box">
        <image class="app-logo-icon" src="/icon.png" mode="aspectFit" />
        <text class="title">{{skinTitle}}</text>
      </view>

      <!-- Skin Selector Menu Buttons -->
      <view class="skin-selector">
        <view class="skin-btn {{skinMode === 'skin-penguin' ? 'active' : ''}}" bindtap="onSelectSkin" data-skin="skin-penguin">🐧企鹅</view>
        <view class="skin-btn {{skinMode === 'skin-bear' ? 'active' : ''}}" bindtap="onSelectSkin" data-skin="skin-bear">🐻小熊</view>
        <view class="skin-btn {{skinMode === 'skin-aurora' ? 'active' : ''}}" bindtap="onSelectSkin" data-skin="skin-aurora">🌌赛博</view>
        <view class="skin-btn history-btn" bindtap="onToggleHistory">📜历史</view>
      </view>
    </view>

    <!-- Display Screen -->
    <view class="calc-display">
      <scroll-view scroll-x class="expr-scroll">
        <text class="expression">{{subDisplay}}</text>
      </scroll-view>
      <text class="main-screen">{{mainDisplay}}</text>
    </view>

    <!-- Function Mode Tabs + DEG/RAD Switcher -->
    <view class="mode-tabs">
      <view class="tab-left">
        <text class="tab-item {{isSciMode ? 'active' : ''}}" bindtap="onToggleSciMode">高阶函数</text>
        <text class="tab-item {{!isSciMode ? 'active' : ''}}" bindtap="onToggleSciMode">基础计算</text>
      </view>
      <view class="tab-right">
        <text class="angle-btn" bindtap="onToggleAngleMode">{{angleMode === 'DEG' ? '📐 角度(DEG)' : '🌐 弧度(RAD)'}}</text>
      </view>
    </view>

    <!-- Scientific Function Keys Row (5 Keys) -->
    <view class="keypad-sci" wx:if="{{isSciMode}}">
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="sin(">sin</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="cos(">cos</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="tan(">tan</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="ln(">ln</view>
      <view class="btn-key sci" hover-class="btn-hover" bindtap="onTapKey" data-val="log(">log</view>
    </view>

    <!-- Main Grid Layout (5 Columns x 5 Rows) -->
    <view class="keypad-grid">
      <!-- Row 1: AC, ⌫ 撤销, (, ), ÷ -->
      <view class="btn-key func-clear" hover-class="btn-hover" bindtap="onClear">AC</view>
      <view class="btn-key func-del" hover-class="btn-hover" bindtap="onDelete">⌫ 撤销</view>
      <view class="btn-key func" hover-class="btn-hover" bindtap="onTapKey" data-val="(">(</view>
      <view class="btn-key func" hover-class="btn-hover" bindtap="onTapKey" data-val=")">)</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="÷">÷</view>

      <!-- Row 2: 7, 8, 9, %, × -->
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="7">7</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="8">8</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="9">9</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="%">%</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="×">×</view>

      <!-- Row 3: 4, 5, 6, ^, - -->
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="4">4</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="5">5</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="6">6</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="^">x^y</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="-">-</view>

      <!-- Row 4: 1, 2, 3, √, + -->
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="1">1</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="2">2</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val="3">3</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="√(">√</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="+">+</view>

      <!-- Row 5: 0 (span 2), ., π, = -->
      <view class="btn-key num span-2" hover-class="btn-hover" bindtap="onTapKey" data-val="0">0</view>
      <view class="btn-key num" hover-class="btn-hover" bindtap="onTapKey" data-val=".">.</view>
      <view class="btn-key op" hover-class="btn-hover" bindtap="onTapKey" data-val="π">π</view>
      <view class="btn-key btn-equal" hover-class="btn-hover" bindtap="onCalculate">=</view>
    </view>
  </view>

  <!-- History Drawer Panel -->
  <view class="history-panel" wx:if="{{showHistory}}">
    <view class="panel-header">
      <text class="panel-title">📜 计算历史记录</text>
      <view class="panel-btns">
        <text class="btn-text-danger" bindtap="onClearHistory">清空历史</text>
        <text class="btn-text-close" bindtap="onToggleHistory">关闭</text>
      </view>
    </view>

    <scroll-view scroll-y class="history-list">
      <block wx:for="{{historyList}}" wx:key="index">
        <view class="history-item" bindtap="onSelectHistory" data-item="{{item}}">
          <text class="h-expr">{{item.expr}}</text>
          <text class="h-res">= {{item.res}}</text>
        </view>
      </block>
      <view class="empty-tip" wx:if="{{historyList.length === 0}}">
        <text>暂无历史计算记录</text>
      </view>
    </scroll-view>
  </view>
</view>
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.wxml'), 'w', encoding='utf-8') as f:
    f.write(index_wxml)

# 2. Update index.js smart onDelete logic
index_js = """// Pure JavaScript Safe Math Parser & Evaluator for WeChat Mini Program (Zero eval / new Function!)

function safeEvalMath(expr, angleMode = 'DEG') {
  if (!expr) return null;
  let text = String(expr).trim();
  if (!text) return null;

  // Auto-close missing right parentheses ')'
  let openCount = (text.match(/\\(/g) || []).length;
  let closeCount = (text.match(/\\)/g) || []).length;
  while (openCount > closeCount) {
    text += ')';
    closeCount++;
  }

  // Tokenize & Normalize
  text = text
    .replace(/×/g, '*')
    .replace(/÷/g, '/')
    .replace(/π/g, String(Math.PI))
    .replace(/e/g, String(Math.E))
    .replace(/√\\(/g, 'sqrt(')
    .replace(/√(\\d+(\\.\\d+)?)/g, 'sqrt($1)');

  const tokens = [];
  let i = 0;
  while (i < text.length) {
    let ch = text[i];
    if (/\\s/.test(ch)) { i++; continue; }

    // Numbers
    if (/[\\d.]/.test(ch)) {
      let numStr = '';
      while (i < text.length && /[\\d.]/.test(text[i])) {
        numStr += text[i];
        i++;
      }
      tokens.push({ type: 'NUM', value: parseFloat(numStr) });
      continue;
    }

    // Function names (sin, cos, tan, ln, log, sqrt)
    if (/[a-zA-Z_]/.test(ch)) {
      let name = '';
      while (i < text.length && /[a-zA-Z_]/.test(text[i])) {
        name += text[i];
        i++;
      }
      tokens.push({ type: 'FUNC', value: name });
      continue;
    }

    // Operators and Parentheses (+, -, *, /, ^, %, (, ))
    if (['+', '-', '*', '/', '^', '%', '(', ')'].includes(ch)) {
      if (ch === '-') {
        const prev = tokens[tokens.length - 1];
        if (!prev || prev.value === '(' || prev.type === 'OP') {
          tokens.push({ type: 'NUM', value: 0 });
        }
      }
      tokens.push({ type: ch === '(' || ch === ')' ? 'PAREN' : 'OP', value: ch });
      i++;
      continue;
    }

    i++;
  }

  // Shunting-yard algorithm -> RPN
  const precedence = { '+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3 };
  const rightAssoc = { '^': true };

  const outputQueue = [];
  const operatorStack = [];

  for (let t of tokens) {
    if (t.type === 'NUM') {
      outputQueue.push(t);
    } else if (t.type === 'FUNC') {
      operatorStack.push(t);
    } else if (t.type === 'OP') {
      while (operatorStack.length > 0) {
        let top = operatorStack[operatorStack.length - 1];
        if (top.type === 'FUNC') {
          outputQueue.push(operatorStack.pop());
        } else if (top.type === 'OP') {
          let p1 = precedence[t.value];
          let p2 = precedence[top.value];
          if ((!rightAssoc[t.value] && p1 <= p2) || (rightAssoc[t.value] && p1 < p2)) {
            outputQueue.push(operatorStack.pop());
          } else {
            break;
          }
        } else {
          break;
        }
      }
      operatorStack.push(t);
    } else if (t.value === '(') {
      operatorStack.push(t);
    } else if (t.value === ')') {
      while (operatorStack.length > 0 && operatorStack[operatorStack.length - 1].value !== '(') {
        outputQueue.push(operatorStack.pop());
      }
      if (operatorStack.length > 0 && operatorStack[operatorStack.length - 1].value === '(') {
        operatorStack.pop();
      }
      if (operatorStack.length > 0 && operatorStack[operatorStack.length - 1].type === 'FUNC') {
        outputQueue.push(operatorStack.pop());
      }
    }
  }

  while (operatorStack.length > 0) {
    outputQueue.push(operatorStack.pop());
  }

  // RPN Evaluator
  const evalStack = [];
  for (let t of outputQueue) {
    if (t.type === 'NUM') {
      evalStack.push(t.value);
    } else if (t.type === 'OP') {
      if (evalStack.length < 2) return null;
      let b = evalStack.pop();
      let a = evalStack.pop();
      let res = 0;
      switch (t.value) {
        case '+': res = a + b; break;
        case '-': res = a - b; break;
        case '*': res = a * b; break;
        case '/': res = b === 0 ? NaN : a / b; break;
        case '%': res = a % b; break;
        case '^': res = Math.pow(a, b); break;
      }
      evalStack.push(res);
    } else if (t.type === 'FUNC') {
      if (evalStack.length < 1) return null;
      let a = evalStack.pop();
      let res = 0;
      const fname = t.value.toLowerCase();
      if (fname === 'sin') {
        res = angleMode === 'DEG' ? Math.sin(a * Math.PI / 180) : Math.sin(a);
      } else if (fname === 'cos') {
        res = angleMode === 'DEG' ? Math.cos(a * Math.PI / 180) : Math.cos(a);
      } else if (fname === 'tan') {
        res = angleMode === 'DEG' ? Math.tan(a * Math.PI / 180) : Math.tan(a);
      } else if (fname === 'ln') {
        res = Math.log(a);
      } else if (fname === 'log') {
        res = Math.log10(a);
      } else if (fname === 'sqrt') {
        res = Math.sqrt(a);
      }
      if (typeof res === 'number' && Math.abs(res) < 1e-12) res = 0;
      evalStack.push(res);
    }
  }

  if (evalStack.length === 1 && !isNaN(evalStack[0]) && isFinite(evalStack[0])) {
    return evalStack[0];
  }
  return null;
}

Page({
  data: {
    expression: '',
    mainDisplay: '0',
    subDisplay: '',
    isSciMode: true,
    angleMode: 'DEG',
    showHistory: false,
    historyList: [],
    skinMode: 'skin-penguin',
    skinTitle: '企鹅宝宝计算器',
    isEvaluated: false
  },

  onLoad() {
    const historyList = wx.getStorageSync('calc_history_v1') || [];
    const skinMode = wx.getStorageSync('calc_skin_v1') || 'skin-penguin';
    this.applySkin(skinMode);
    this.setData({ historyList });
  },

  applySkin(skin) {
    let title = '企鹅宝宝计算器';
    if (skin === 'skin-bear') title = '可爱小熊计算器';
    if (skin === 'skin-aurora') title = '极光赛博计算器';

    this.setData({
      skinMode: skin,
      skinTitle: title
    });
    wx.setStorageSync('calc_skin_v1', skin);
  },

  onSelectSkin(e) {
    const skin = e.currentTarget.dataset.skin;
    this.applySkin(skin);
  },

  onToggleSciMode() {
    this.setData({ isSciMode: !this.data.isSciMode });
  },

  onToggleAngleMode() {
    const angleMode = this.data.angleMode === 'DEG' ? 'RAD' : 'DEG';
    this.setData({ angleMode });
    if (this.data.expression) {
      this.autoPreview(this.data.expression);
    }
  },

  onToggleHistory() {
    this.setData({ showHistory: !this.data.showHistory });
  },

  onClearHistory() {
    wx.removeStorageSync('calc_history_v1');
    this.setData({ historyList: [] });
  },

  onSelectHistory(e) {
    const { item } = e.currentTarget.dataset;
    this.setData({
      expression: item.expr,
      mainDisplay: item.res,
      subDisplay: item.expr + ' =',
      isEvaluated: true,
      showHistory: false
    });
  },

  onTapKey(e) {
    const val = e.currentTarget.dataset.val;
    let expr = this.data.expression;

    if (this.data.isEvaluated) {
      if (/^[0-9.πe]$/.test(val) || val.includes('(')) {
        expr = '';
      }
      this.setData({ isEvaluated: false });
    }

    expr += val;
    this.setData({
      expression: expr,
      mainDisplay: expr,
      subDisplay: ''
    });

    this.autoPreview(expr);
  },

  onClear() {
    this.setData({
      expression: '',
      mainDisplay: '0',
      subDisplay: '',
      isEvaluated: false
    });
  },

  onDelete() {
    let expr = this.data.expression;
    if (this.data.isEvaluated) {
      this.onClear();
      return;
    }
    if (expr.length > 0) {
      // Smart Undo: Delete function names like sin(, cos(, tan(, log(, ln(, √() as a whole unit
      if (/(sin\(|cos\(|tan\(|log\(|sqrt\(|ln\(|√\()$/.test(expr)) {
        expr = expr.replace(/(sin\(|cos\(|tan\(|log\(|sqrt\(|ln\(|√\()$/, '');
      } else {
        expr = expr.slice(0, -1);
      }

      this.setData({
        expression: expr,
        mainDisplay: expr || '0',
        subDisplay: ''
      });

      if (expr) this.autoPreview(expr);
      else this.setData({ subDisplay: '' });
    }
  },

  autoPreview(expr) {
    if (!expr) return;
    try {
      let res = safeEvalMath(expr, this.data.angleMode);
      if (res !== null && !isNaN(res) && isFinite(res)) {
        const previewStr = '= ' + String(parseFloat(res.toFixed(8)));
        this.setData({ subDisplay: previewStr });
      }
    } catch (e) {}
  },

  onCalculate() {
    const expr = this.data.expression;
    if (!expr) return;
    try {
      let res = safeEvalMath(expr, this.data.angleMode);
      if (res !== null && !isNaN(res) && isFinite(res)) {
        const resStr = String(parseFloat(res.toFixed(8)));

        let historyList = this.data.historyList;
        historyList.unshift({ expr, res: resStr });
        if (historyList.length > 50) historyList = historyList.slice(0, 50);
        wx.setStorageSync('calc_history_v1', historyList);

        this.setData({
          mainDisplay: resStr,
          subDisplay: expr + ' =',
          expression: resStr,
          isEvaluated: true,
          historyList
        });
      } else {
        this.setData({ mainDisplay: '语法错误', subDisplay: expr });
      }
    } catch (e) {
      this.setData({ mainDisplay: '语法错误', subDisplay: expr });
    }
  }
})
"""
with open(os.path.join(base_dir, 'pages', 'index', 'index.js'), 'w', encoding='utf-8') as f:
    f.write(index_js)

# 3. Update index.wxss to add distinct styling for func-del
index_wxss_append = """
.func-del {
  background: rgba(245, 158, 11, 0.2) !important;
  color: #f59e0b !important;
  font-size: 24rpx !important;
  border: 1rpx solid rgba(245, 158, 11, 0.3) !important;
}
.skin-penguin .func-del {
  background: #fef3c7 !important;
  color: #d97706 !important;
  border-color: #fde68a !important;
  box-shadow: 0 4rpx 0 #fcd34d !important;
}
.skin-bear .func-del {
  background: #fde68a !important;
  color: #b45309 !important;
  border-color: #f59e0b !important;
  box-shadow: 0 4rpx 0 #d97706 !important;
}
"""

with open(os.path.join(base_dir, 'pages', 'index', 'index.wxss'), 'a', encoding='utf-8') as f:
    f.write(index_wxss_append)

print("Added prominent Undo (⌫ 撤销) button with smart delete logic to calculator mini program successfully!")
