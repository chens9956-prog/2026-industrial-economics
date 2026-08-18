// Pure JavaScript Safe Math Parser & Evaluator for WeChat Mini Program (Zero eval / new Function!)

function safeEvalMath(expr, angleMode = 'DEG') {
  if (!expr) return null;
  let text = String(expr).trim();
  if (!text) return null;

  // Auto-close missing right parentheses ')'
  let openCount = (text.match(/\(/g) || []).length;
  let closeCount = (text.match(/\)/g) || []).length;
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
    .replace(/√\(/g, 'sqrt(')
    .replace(/√(\d+(\.\d+)?)/g, 'sqrt($1)');

  const tokens = [];
  let i = 0;
  while (i < text.length) {
    let ch = text[i];
    if (/\s/.test(ch)) { i++; continue; }

    // Numbers
    if (/[\d.]/.test(ch)) {
      let numStr = '';
      while (i < text.length && /[\d.]/.test(text[i])) {
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
