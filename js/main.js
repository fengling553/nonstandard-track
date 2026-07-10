/* ==========================================
   个性化成长教育导航 - 全局逻辑
   ========================================== */

// ===== 导航栏滚动效果 =====
(function() {
  var navbar = document.querySelector('.navbar');
  if (!navbar) return;
  
  window.addEventListener('scroll', function() {
    if (window.scrollY > 10) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
})();

// ===== 移动端菜单切换 =====
(function() {
  var toggle = document.querySelector('.navbar-toggle');
  var menu = document.querySelector('.mobile-menu');
  if (!toggle || !menu) return;
  
  toggle.addEventListener('click', function() {
    toggle.classList.toggle('active');
    menu.classList.toggle('active');
  });
  
  // 点击链接后关闭菜单
  var links = menu.querySelectorAll('a');
  links.forEach(function(link) {
    link.addEventListener('click', function() {
      toggle.classList.remove('active');
      menu.classList.remove('active');
    });
  });
})();

// ===== Tab切换逻辑 =====
function initTabs(tabNavSelector, tabContentPrefix) {
  var tabNav = document.querySelector(tabNavSelector);
  if (!tabNav) return;
  
  var buttons = tabNav.querySelectorAll('.tab-btn');
  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var tabId = this.getAttribute('data-tab');
      
      // 切换按钮状态
      buttons.forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');
      
      // 切换内容
      var contents = document.querySelectorAll('.tab-content');
      contents.forEach(function(c) { c.classList.remove('active'); });
      var target = document.getElementById(tabContentPrefix + tabId);
      if (target) target.classList.add('active');
    });
  });
}

// ===== 层级切换逻辑（训练场） =====
function initLevelNav(levelNavSelector, contentPrefix) {
  var levelNav = document.querySelector(levelNavSelector);
  if (!levelNav) return;
  
  var buttons = levelNav.querySelectorAll('.level-btn');
  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var levelId = this.getAttribute('data-level');
      
      // 切换按钮状态
      buttons.forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');
      
      // 切换内容
      var contents = document.querySelectorAll('.level-content');
      contents.forEach(function(c) { c.classList.remove('active'); });
      var target = document.getElementById(contentPrefix + levelId);
      if (target) target.classList.add('active');
    });
  });
}

// ===== 数据加载 =====
function loadData(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          callback(null, data);
        } catch (e) {
          callback('JSON解析失败: ' + e.message);
        }
      } else {
        callback('加载失败: HTTP ' + xhr.status);
      }
    }
  };
  xhr.send();
}

// ===== 路径情报站渲染 =====
function renderPaths(data) {
  var container = document.getElementById('paths-content');
  if (!container || !data || !data.tabs) return;
  
  var html = '';
  data.tabs.forEach(function(tab, index) {
    var activeClass = index === 0 ? ' active' : '';
    
    html += '<div class="tab-content' + activeClass + '" id="tab-' + tab.id + '">';
    
    // 概述
    html += '<div class="path-overview">';
    html += '<h3>' + tab.icon + ' ' + tab.name + '</h3>';
    html += '<p>' + tab.overview + '</p>';
    html += '<div class="path-meta">';
    html += '<div class="path-meta-item"><div class="meta-label">适合谁</div><div class="meta-value">' + tab.suitableFor + '</div></div>';
    html += '<div class="path-meta-item"><div class="meta-label">核心门槛</div><div class="meta-value">' + tab.coreThreshold + '</div></div>';
    html += '<div class="path-meta-item"><div class="meta-label">关键时间线</div><div class="meta-value">' + tab.timeline + '</div></div>';
    html += '</div></div>';
    
    // 关键节点时间轴
    if (tab.keyNodes && tab.keyNodes.length > 0) {
      html += '<div class="section-group"><h3>📅 关键节点</h3>';
      html += '<div class="timeline">';
      tab.keyNodes.forEach(function(node) {
        html += '<div class="timeline-item">';
        html += '<div class="time-label">' + node.time + '</div>';
        html += '<div class="time-event">' + node.event + '</div>';
        html += '<div class="time-detail">' + node.detail + '</div>';
        html += '</div>';
      });
      html += '</div></div>';
    }
    
    // 详细分类
    if (tab.sections && tab.sections.length > 0) {
      tab.sections.forEach(function(section) {
        html += '<div class="section-group">';
        html += '<h3>📌 ' + section.title + '</h3>';
        section.items.forEach(function(item) {
          html += '<div class="item-card">';
          html += '<h4>' + item.name + '</h4>';
          if (item.highlight) {
            html += '<div class="item-highlight">💡 ' + item.highlight + '</div>';
          }
          html += '<div class="item-desc">' + item.description + '</div>';
          if (item.requirement) {
            html += '<div class="item-requirement">📋 报名条件：' + item.requirement + '</div>';
          }
          if (item.url) {
            html += '<div class="item-url"><a href="' + item.url + '" target="_blank" rel="noopener">访问链接 ↗</a></div>';
          }
          html += '</div>';
        });
        html += '</div>';
      });
    }
    
    // 真实案例
    if (tab.cases && tab.cases.length > 0) {
      html += '<div class="section-group"><h3>👤 真实案例</h3>';
      tab.cases.forEach(function(c) {
        html += '<div class="case-card">';
        html += '<div class="case-name">' + c.name + '</div>';
        html += '<div class="case-age">年龄：' + c.age + '岁</div>';
        html += '<div class="case-story">' + c.story + '</div>';
        html += '<div class="case-result">✅ ' + c.result + '</div>';
        html += '</div>';
      });
      html += '</div>';
    }
    
    // 入门指南
    if (tab.starterGuide) {
      html += '<div class="starter-guide">';
      html += '<h3>🎯 入门指南</h3>';
      html += '<ol>';
      var steps = tab.starterGuide.split('\n');
      steps.forEach(function(step) {
        if (step.trim()) {
          html += '<li>' + step.replace(/^\d+\.\s*/, '') + '</li>';
        }
      });
      html += '</ol></div>';
    }
    
    // 资源链接
    if (tab.resources && tab.resources.length > 0) {
      html += '<div class="resource-links">';
      html += '<h3>🔗 相关资源</h3>';
      tab.resources.forEach(function(r) {
        html += '<div class="resource-link-item">';
        html += '<span class="link-icon">🌐</span>';
        html += '<span class="link-name">';
        if (r.url) {
          html += '<a href="' + r.url + '" target="_blank" rel="noopener">' + r.name + '</a>';
        } else {
          html += r.name;
        }
        html += '</span>';
        html += '<span class="link-desc">' + r.description + '</span>';
        html += '</div>';
      });
      html += '</div>';
    }
    
    // 更新时间
    html += '<div class="update-info">📅 最近更新：' + (tab.updatedAt || data.updatedAt) + '</div>';
    
    html += '</div>';
  });
  
  container.innerHTML = html;
}

// ===== 学科卡片渲染 =====
function renderSubjects(data) {
  var container = document.getElementById('subjects-grid');
  if (!container || !data || !data.subjects) return;
  
  var html = '';
  data.subjects.forEach(function(subject) {
    var cardClass = subject.available ? 'subject-card available' : 'subject-card coming-soon';
    var badgeText = subject.available ? '已上线 · L1-L5' : subject.comingSoon;
    var clickAttr = subject.available ? ' onclick="location.href=\'' + (subject.id === 'math' ? 'math-training.html' : subject.id === 'physics' ? 'physics-training.html' : '#') + '\'"' : '';
    
    html += '<div class="' + cardClass + '"' + clickAttr + '>';
    html += '<div class="subject-icon">' + subject.icon + '</div>';
    html += '<h3>' + subject.name + '</h3>';
    html += '<div class="subject-desc">' + subject.description + '</div>';
    html += '<span class="subject-badge">' + badgeText + '</span>';
    html += '</div>';
  });
  
  container.innerHTML = html;
}

// ===== 训练场资源渲染 =====
function renderTrainingResources(data) {
  var container = document.getElementById('training-content');
  if (!container || !data || !data.levels) return;
  
  var typeNames = {
    'book': '📚 书籍推荐',
    'local': '📍 深圳本地',
    'online': '💻 线上训练营',
    'course': '🎓 名师课程'
  };
  
  var typeIcons = {
    'book': '📚',
    'local': '📍',
    'online': '💻',
    'course': '🎓'
  };
  
  var html = '';
  data.levels.forEach(function(level, index) {
    var activeClass = index === 0 ? ' active' : '';
    html += '<div class="level-content' + activeClass + '" id="level-' + level.id + '">';
    
    // 层级说明
    html += '<div class="level-description">';
    html += '<span class="level-badge">' + level.id + '</span>';
    html += '<div class="level-info">';
    html += '<h3>' + level.name + '</h3>';
    html += '<p>' + level.description + ' · ' + level.ageRange + '</p>';
    html += '</div></div>';
    
    // 按资源类型分组
    var grouped = {};
    level.resources.forEach(function(r) {
      if (!grouped[r.type]) grouped[r.type] = [];
      grouped[r.type].push(r);
    });
    
    var typeOrder = ['book', 'local', 'online', 'course'];
    typeOrder.forEach(function(type) {
      if (!grouped[type]) return;
      var resources = grouped[type];
      
      html += '<div class="resource-type-group">';
      html += '<div class="resource-type-header">';
      html += '<span class="type-icon">' + typeIcons[type] + '</span>';
      html += '<h3>' + typeNames[type] + '</h3>';
      html += '<span class="type-count">' + resources.length + '项</span>';
      html += '</div>';
      
      resources.forEach(function(r) {
        var tagClass = '';
        if (r.price && (r.price.indexOf('免费') >= 0 || r.price.indexOf('free') >= 0 || r.price === '免费')) {
          tagClass = 'tag-free';
        } else {
          tagClass = 'tag-paid';
        }
        
        var typeTagClass = 'tag-' + r.type;
        
        html += '<div class="resource-card">';
        html += '<div class="card-header">';
        html += '<h4>' + r.title + '</h4>';
        if (r.price) {
          html += '<span class="card-price">' + r.price + '</span>';
        }
        html += '</div>';
        html += '<div class="card-desc">' + r.description + '</div>';
        if (r.detail) {
          html += '<div class="card-detail">' + r.detail + '</div>';
        }
        html += '<div class="card-tags">';
        if (r.tags) {
          r.tags.forEach(function(tag) {
            html += '<span class="tag ' + tagClass + '">' + tag + '</span>';
          });
        }
        html += '<span class="tag ' + typeTagClass + '">' + typeNames[r.type].replace(/^[^\s]+\s/, '') + '</span>';
        html += '</div>';
        if (r.language) {
          html += '<div class="card-lang">🌐 语言：' + r.language + '</div>';
        }
        if (r.url) {
          html += '<div class="card-url"><a href="' + r.url + '" target="_blank" rel="noopener">访问链接 ↗</a></div>';
        }
        html += '</div>';
      });
      
      html += '</div>';
    });
    
    // 更新时间
    html += '<div class="update-info">📅 最近更新：' + (level.updatedAt || data.updatedAt) + '</div>';
    
    html += '</div>';
  });
  
  container.innerHTML = html;
}

// ===== AI浮动按钮 =====
(function() {
  var fab = document.querySelector('.ai-fab');
  var tooltip = document.querySelector('.ai-fab-tooltip');
  if (!fab) return;
  
  fab.addEventListener('click', function() {
    if (tooltip) {
      tooltip.classList.toggle('show');
      // 3秒后自动隐藏
      setTimeout(function() {
        if (tooltip.classList.contains('show')) {
          tooltip.classList.remove('show');
        }
      }, 3000);
    }
  });
  
  // 点击其他地方隐藏
  document.addEventListener('click', function(e) {
    if (!fab.contains(e.target) && tooltip && !tooltip.contains(e.target)) {
      tooltip.classList.remove('show');
    }
  });
})();

// ===== 平滑滚动到锚点 =====
document.addEventListener('DOMContentLoaded', function() {
  var anchors = document.querySelectorAll('a[href^="#"]');
  anchors.forEach(function(a) {
    a.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        var offset = 80; // 导航栏高度
        var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });
});

// ===== 返回顶部 =====
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
