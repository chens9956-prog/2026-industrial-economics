// Pure JavaScript Safe Math Parser & Evaluator (Zero eval / new Function!)

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

document.addEventListener('DOMContentLoaded', () => {

    let expression = '';
    let resultStr = '0';
    let history = JSON.parse(localStorage.getItem('calc_history_v1') || '[]');
    let currentSkin = localStorage.getItem('calc_skin_v1') || 'penguin';
    let isDeg = true;

    const displayExpr = document.getElementById('display-expr');
    const displayRes = document.getElementById('display-res');
    const historyContainer = document.getElementById('history-list-container');
    const btnClearHistory = document.getElementById('btn-clear-history');
    const skinAvatarIcon = document.getElementById('skin-avatar-icon');
    const skinTitleText = document.getElementById('skin-title-text');
    const appBody = document.getElementById('app-body');
    const calcCard = document.getElementById('calc-card');

    // --- Skin Switcher ---
    const applySkin = (skin) => {
        currentSkin = skin;
        localStorage.setItem('calc_skin_v1', skin);

        document.querySelectorAll('.skin-btn').forEach(btn => {
            if (btn.getAttribute('data-skin') === skin) {
                btn.className = 'skin-btn active px-3 py-1.5 rounded-xl text-xs font-bold transition-all bg-sky-500 text-white flex items-center gap-1 shadow-md';
            } else {
                btn.className = 'skin-btn px-3 py-1.5 rounded-xl text-xs font-bold transition-all text-slate-300 hover:bg-slate-800 flex items-center gap-1';
            }
        });

        if (skin === 'penguin') {
            skinAvatarIcon.textContent = '🐧';
            skinTitleText.textContent = '企鹅宝宝科学计算器';
            appBody.className = 'bg-gradient-to-br from-slate-900 via-sky-950 to-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4 selection:bg-sky-500 selection:text-white relative overflow-x-hidden font-sans transition-all duration-500';
            calcCard.className = 'lg:col-span-8 bg-white/95 text-slate-900 backdrop-blur-2xl border-4 border-sky-400 rounded-3xl p-6 shadow-2xl space-y-5 transition-all';
        } else if (skin === 'bear') {
            skinAvatarIcon.textContent = '🐻';
            skinTitleText.textContent = '可爱小熊科学计算器';
            appBody.className = 'bg-gradient-to-br from-amber-950 via-stone-900 to-amber-900 text-slate-100 min-h-screen flex items-center justify-center p-4 selection:bg-amber-500 selection:text-white relative overflow-x-hidden font-sans transition-all duration-500';
            calcCard.className = 'lg:col-span-8 bg-amber-50/95 text-amber-950 backdrop-blur-2xl border-4 border-amber-500 rounded-3xl p-6 shadow-2xl space-y-5 transition-all';
        } else {
            skinAvatarIcon.textContent = '🧮';
            skinTitleText.textContent = '极光赛博科学计算器';
            appBody.className = 'bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-4 selection:bg-indigo-500 selection:text-white relative overflow-x-hidden font-sans transition-all duration-500';
            calcCard.className = 'lg:col-span-8 bg-slate-900/80 text-white backdrop-blur-2xl border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-5 transition-all';
        }
    };

    document.querySelectorAll('.skin-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const skin = btn.getAttribute('data-skin');
            applySkin(skin);
        });
    });

    applySkin(currentSkin);

    const updateDisplay = () => {
        displayExpr.textContent = expression || '0';
        displayRes.textContent = '= ' + resultStr;
    };

    const autoEval = (expr) => {
        if (!expr) {
            resultStr = '0';
            updateDisplay();
            return;
        }
        try {
            const res = safeEvalMath(expr, isDeg ? 'DEG' : 'RAD');
            if (res !== null && !isNaN(res) && isFinite(res)) {
                resultStr = String(parseFloat(res.toFixed(8)));
            }
        } catch (e) {}
        updateDisplay();
    };

    // Button clicks
    document.querySelectorAll('.btn-calc[data-val]').forEach(btn => {
        btn.addEventListener('click', () => {
            const val = btn.getAttribute('data-val');
            expression += val;
            autoEval(expression);
        });
    });

    document.getElementById('btn-clear').addEventListener('click', () => {
        expression = '';
        resultStr = '0';
        updateDisplay();
    });

    document.getElementById('btn-del').addEventListener('click', () => {
        if (expression.length > 0) {
            expression = expression.slice(0, -1);
            autoEval(expression);
        }
    });

    document.getElementById('btn-equal').addEventListener('click', () => {
        if (!expression) return;
        try {
            const res = safeEvalMath(expression, isDeg ? 'DEG' : 'RAD');
            if (res !== null && !isNaN(res) && isFinite(res)) {
                resultStr = String(parseFloat(res.toFixed(8)));
                history.unshift({ expr: expression, res: resultStr });
                if (history.length > 50) history = history.slice(0, 50);
                localStorage.setItem('calc_history_v1', JSON.stringify(history));
                renderHistory();
            } else {
                resultStr = '语法错误';
            }
        } catch (e) {
            resultStr = '语法错误';
        }
        updateDisplay();
    });

    const renderHistory = () => {
        if (history.length === 0) {
            historyContainer.innerHTML = `<div class="text-center text-slate-500 py-8">暂无历史计算记录</div>`;
            return;
        }
        historyContainer.innerHTML = history.map((item, idx) => `
            <div data-idx="${idx}" class="history-item p-3 bg-slate-950/60 border border-slate-800 rounded-xl cursor-pointer hover:border-sky-500/50 transition-all flex items-center justify-between">
                <span class="text-slate-400">${item.expr}</span>
                <span class="font-bold text-sky-400">= ${item.res}</span>
            </div>
        `).join('');

        document.querySelectorAll('.history-item').forEach(itemEl => {
            itemEl.addEventListener('click', () => {
                const idx = itemEl.getAttribute('data-idx');
                const selected = history[idx];
                if (selected) {
                    expression = selected.expr;
                    resultStr = selected.res;
                    updateDisplay();
                }
            });
        });
    };

    btnClearHistory.addEventListener('click', () => {
        history = [];
        localStorage.removeItem('calc_history_v1');
        renderHistory();
    });

    renderHistory();
});
