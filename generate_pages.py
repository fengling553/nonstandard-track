#!/usr/bin/env python3
"""Generate 7 training field HTML pages and update existing pages."""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE_DIR, 'pages')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Subject configuration: (subjectId, icon, filename, data_file)
SUBJECTS = [
    ('chemistry', '🧪', 'chemistry-training.html', 'chemistry-resources.json'),
    ('biology', '🧬', 'biology-training.html', 'biology-resources.json'),
    ('informatics', '💻', 'informatics-training.html', 'informatics-resources.json'),
    ('english', '🌍', 'english-training.html', 'english-resources.json'),
    ('history', '🏛️', 'history-training.html', 'history-resources.json'),
    ('geography', '🗺️', 'geography-training.html', 'geography-resources.json'),
    ('politics', '⚖️', 'politics-training.html', 'politics-resources.json'),
]

# Type icon mapping
TYPE_ICONS = {'book': '📚', 'local': '📍', 'online': '💻', 'course': '🎓'}
TYPE_NAMES = {'book': '书籍推荐', 'local': '深圳本地', 'online': '线上训练营', 'course': '名师课程'}
TYPE_TAG_CLASSES = {'book': 'tag-book', 'local': 'tag-local', 'online': 'tag-online', 'course': 'tag-course'}

# Tag class mapping
TAG_CLASS_MAP = {
    '免费': 'tag-free', '自学': 'tag-free', '亲子共读': 'tag-free', '基础训练': 'tag-free',
    '公益': 'tag-free', '分级阅读': 'tag-free', '课内延伸': 'tag-free', '读写结合': 'tag-free',
    '中文': 'tag-free', '中文/英文': 'tag-free',
    '付费': 'tag-paid', '线下': 'tag-paid', '体系课': 'tag-paid', 'AI辅助': 'tag-paid',
    '福田区': 'tag-paid', '福田/宝安/龙华': 'tag-paid', '文言文经典': 'tag-paid',
    '作文实战': 'tag-paid', '底层逻辑': 'tag-paid', '初高衔接': 'tag-paid',
    '大学先修': 'tag-paid', '文学理论': 'tag-paid', '经典': 'tag-free', '思辨': 'tag-free',
    '方法论': 'tag-free',
}


def generate_tag_html(tag):
    """Generate a tag span HTML for a resource tag."""
    tag_class = TAG_CLASS_MAP.get(tag, 'tag-free')
    return f'<span class="tag {tag_class}">{tag}</span>'


def generate_resource_card_html(resource):
    """Generate HTML for a single resource card."""
    title = resource.get('title', '')
    price = resource.get('price', '')
    desc = resource.get('description', '')
    detail = resource.get('detail', '')
    tags = resource.get('tags', [])
    url = resource.get('url', '')
    language = resource.get('language', '')
    res_type = resource.get('type', 'book')

    html = '            <div class="resource-card">\n'

    # Header with title and price
    html += f'              <div class="card-header"><h4>{title}</h4><span class="card-price">{price}</span></div>\n'

    # Description
    html += f'              <div class="card-desc">{desc}</div>\n'

    # Detail
    if detail:
        html += f'              <div class="card-detail">{detail}</div>\n'

    # Tags
    tags_html = ' '.join(generate_tag_html(t) for t in tags)
    html += f'              <div class="card-tags">{tags_html}</div>\n'

    # Language
    if language:
        html += f'              <div class="card-lang">🌐 语言：{language}</div>\n'

    # URL
    if url and url.startswith('http'):
        html += f'              <div class="card-url"><a href="{url}" target="_blank" rel="noopener">访问链接 ↗</a></div>\n'

    html += '            </div>\n'
    return html


def generate_level_content_html(level_data, subject_name):
    """Generate HTML for a level content section."""
    level_id = level_data['id']
    level_name = level_data['name']
    description = level_data['description']
    age_range = level_data['ageRange']
    resources = level_data.get('resources', [])

    html = f'        <!-- {level_id} {level_name} -->\n'
    html += f'        <div class="level-content" id="level-{level_id}">\n'
    html += '          <div class="level-description">\n'
    html += f'            <span class="level-badge">{level_id}</span>\n'
    html += '            <div class="level-info">\n'
    html += f'              <h3>{level_name}</h3>\n'
    html += f'              <p>{description} · {age_range}</p>\n'
    html += '            </div>\n'
    html += '          </div>\n\n'

    # Group resources by type
    type_order = ['book', 'local', 'online', 'course']
    for res_type in type_order:
        type_resources = [r for r in resources if r.get('type') == res_type]
        if not type_resources:
            continue

        type_icon = TYPE_ICONS[res_type]
        type_name = TYPE_NAMES[res_type]
        count = len(type_resources)

        html += '          <div class="resource-type-group">\n'
        html += f'            <div class="resource-type-header"><span class="type-icon">{type_icon}</span><h3>{type_name}</h3><span class="type-count">{count}项</span></div>\n'

        for resource in type_resources:
            html += generate_resource_card_html(resource)

        html += '          </div>\n\n'

    html += '          <div class="update-info">📅 最近更新：2026-07-09</div>\n'
    html += '        </div>\n\n'
    return html


def generate_training_page(template_html, subject_data, subject_id, icon):
    """Generate a training field HTML page from the template and data."""
    subject_name = subject_data['subject']
    intro = subject_data['intro']
    levels = subject_data['levels']

    html = template_html

    # Replace title
    html = html.replace('<title>语文训练场 - 非标赛道</title>',
                        f'<title>{subject_name}训练场 - 非标赛道</title>')

    # Replace meta description
    html = html.replace('content="语文L1-L5五级进阶训练资源，精选书籍、深圳本地、线上、名师四类资源"',
                        f'content="{subject_name}L1-L5五级进阶训练资源，精选书籍、深圳本地、线上、名师四类资源"')

    # Replace breadcrumb
    html = html.replace('<span class="current">语文训练场</span>',
                        f'<span class="current">{subject_name}训练场</span>')

    # Replace page title
    html = html.replace('<h1>📖 语文训练场</h1>',
                        f'<h1>{icon} {subject_name}训练场</h1>')

    # Replace subtitle
    html = html.replace('<p>从识字阅读到人文素养，五级进阶体系</p>',
                        f'<p>{intro}</p>')

    # Replace level nav buttons
    level_nav_html = f'      <div class="level-nav" id="{subject_id}-level-nav">\n'
    for i, level in enumerate(levels):
        active = ' active' if i == 0 else ''
        level_nav_html += f'        <button class="level-btn{active}" data-level="{level["id"]}">\n'
        level_nav_html += f'          <div class="level-id">{level["id"]}</div>\n'
        level_nav_html += f'          <div class="level-name">{level["name"]}</div>\n'
        level_nav_html += f'          <div class="level-age">{level["ageRange"]}</div>\n'
        level_nav_html += '        </button>\n'
    level_nav_html += '      </div>'

    # Find and replace the level nav section
    old_nav_pattern = r'      <div class="level-nav" id="chinese-level-nav">.*?</div>\s*</div>'
    # More precise: from the level-nav div to its closing
    nav_start = html.find('<div class="level-nav" id="chinese-level-nav">')
    if nav_start != -1:
        # Find the matching end of the level-nav div
        # Count div opens/closes from nav_start
        pos = nav_start
        depth = 0
        found_end = -1
        while pos < len(html):
            if html[pos:pos+4] == '<div':
                depth += 1
            elif html[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    found_end = pos + 6
                    break
            pos += 1
        if found_end != -1:
            html = html[:nav_start] + level_nav_html + html[found_end:]

    # Replace level content sections
    # Find the training-content div and replace its contents
    content_start_marker = '<div id="training-content">'
    content_start = html.find(content_start_marker)
    if content_start != -1:
        content_start += len(content_start_marker)

        # Find the closing </div> of training-content
        pos = content_start
        depth = 1
        content_end = -1
        while pos < len(html):
            if html[pos:pos+4] == '<div':
                depth += 1
            elif html[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    content_end = pos
                    break
            pos += 1

        if content_end != -1:
            # Generate new content
            new_content = '\n'
            for level in levels:
                new_content += generate_level_content_html(level, subject_name)
            new_content += '      '

            html = html[:content_start] + new_content + html[content_end:]

    # Replace JS init call
    html = html.replace("initLevelNav('#chinese-level-nav', 'level-');",
                        f"initLevelNav('#{subject_id}-level-nav', 'level-');")

    # Replace footer source text
    html = html.replace(
        '语文训练资源信息来自各教材/课程官网、豆瓣等公开渠道，具体来源链接已在各资源卡片中标注。',
        f'{subject_name}训练资源信息来自各教材/课程官网、豆瓣等公开渠道，具体来源链接已在各资源卡片中标注。'
    )

    return html


def update_training_html(html):
    """Update training.html to mark 7 subjects as available."""
    # Replace coming-soon cards with available cards for the 7 new subjects
    replacements = {
        'chemistry': ('chemistry-training.html', '元素世界与化学反应的奥秘探索'),
        'biology': ('biology-training.html', '从微观细胞到宏观生态的生命科学'),
        'informatics': ('informatics-training.html', '编程思维与算法竞赛的完整路径'),
        'english': ('english-training.html', '语言能力与国际视野的双向拓展'),
        'history': ('history-training.html', '以史为鉴，培养批判性思维'),
        'geography': ('geography-training.html', '认识世界，理解人地关系'),
        'politics': ('politics-training.html', '公民素养与社会认知的培养'),
    }

    for subject_id, (href, desc) in replacements.items():
        # Find the coming-soon card for this subject and replace it
        old_card_pattern = f'''        <div class="subject-card coming-soon">
          <div class="subject-icon">{SUBJECTS[[s[0] for s in SUBJECTS].index(subject_id)][1]}</div>
          <h3>{subject_id.capitalize() if subject_id not in ["chemistry","biology","informatics","english","history","geography","politics"] else {"chemistry":"化学","biology":"生物","informatics":"信息学","english":"英语","history":"历史","geography":"地理","politics":"政治"}[subject_id]}</h3>
          <div class="subject-desc">{desc}</div>
          <span class="subject-badge">即将上线</span>
        </div>'''

        # Get icon and name
        icon = SUBJECTS[[s[0] for s in SUBJECTS].index(subject_id)][1]
        name_map = {"chemistry":"化学","biology":"生物","informatics":"信息学","english":"英语","history":"历史","geography":"地理","politics":"政治"}
        name = name_map[subject_id]

        new_card = f'''        <div class="subject-card available" onclick="location.href='{href}'">
          <div class="subject-icon">{icon}</div>
          <h3>{name}</h3>
          <div class="subject-desc">{desc}</div>
          <span class="subject-badge">已上线 · L1-L5</span>
        </div>'''

        old_card = f'''        <div class="subject-card coming-soon">
          <div class="subject-icon">{icon}</div>
          <h3>{name}</h3>
          <div class="subject-desc">{desc}</div>
          <span class="subject-badge">即将上线</span>
        </div>'''

        html = html.replace(old_card, new_card)

    # Update the update-info date
    html = html.replace('📅 最近更新：2026-07-08', '📅 最近更新：2026-07-09')

    return html


def generate_assessment_data_js(assessment_data):
    """Generate the ASSESSMENT_DATA JS variable as a string, with no Chinese quotes."""
    # Convert to JSON, then replace Chinese quotes with English single quotes
    json_str = json.dumps(assessment_data, ensure_ascii=False, indent=2)
    # Replace Chinese quotes
    json_str = json_str.replace('\u201c', "'").replace('\u201d', "'")
    json_str = json_str.replace('\u2018', "'").replace('\u2019', "'")
    return f'var ASSESSMENT_DATA = {json_str};'


def generate_resource_data_js():
    """Generate RESOURCE_DATA JS for all 9 subjects."""
    # Load resource data for all subjects
    all_resource_data = {}

    # Math and Chinese already exist in the current assessment.html
    # We need to add data for the 7 new subjects
    subject_files = {
        'chemistry': 'chemistry-resources.json',
        'biology': 'biology-resources.json',
        'informatics': 'informatics-resources.json',
        'english': 'english-resources.json',
        'history': 'history-resources.json',
        'geography': 'geography-resources.json',
        'politics': 'politics-resources.json',
    }

    # First, include existing math and chinese data (will be preserved from existing)
    # Then add new subjects
    for sid, fname in subject_files.items():
        fpath = os.path.join(DATA_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        levels_data = {}
        for level in data['levels']:
            level_id = level['id']
            levels_data[level_id] = {
                'name': level['name'],
                'description': level['description'],
                'ageRange': level['ageRange'],
                'resources': [
                    {
                        'title': r['title'],
                        'type': r['type'],
                        'description': r['description'],
                        'price': r.get('price', '')
                    }
                    for r in level.get('resources', [])[:3]  # Top 3 resources per level
                ]
            }
        all_resource_data[sid] = {'levels': levels_data}

    json_str = json.dumps(all_resource_data, ensure_ascii=False, indent=2)
    json_str = json_str.replace('\u201c', "'").replace('\u201d', "'")
    return f'var NEW_RESOURCE_DATA = {json_str};'


def update_assessment_html(html, assessment_data):
    """Update assessment.html with 9 subjects and expanded ASSESSMENT_DATA."""
    # 1. Replace ASSESSMENT_DATA
    new_assessment_js = generate_assessment_data_js(assessment_data)

    # Find and replace the ASSESSMENT_DATA block
    old_data_start = html.find('var ASSESSMENT_DATA = {')
    if old_data_start != -1:
        # Find the end of the ASSESSMENT_DATA assignment (matching closing };)
        pos = old_data_start + len('var ASSESSMENT_DATA = ')
        depth = 0
        data_end = -1
        while pos < len(html):
            if html[pos] == '{':
                depth += 1
            elif html[pos] == '}':
                depth -= 1
                if depth == 0:
                    # Look for the semicolon
                    if pos + 1 < len(html) and html[pos + 1] == ';':
                        data_end = pos + 2
                    else:
                        data_end = pos + 1
                    break
            pos += 1

        if data_end != -1:
            html = html[:old_data_start] + new_assessment_js + html[data_end:]

    # 2. Add 7 new subject select cards
    new_subject_cards = ''

    # Chemistry
    new_subject_cards += '''
        <div class="subject-select-card" onclick="startQuiz('chemistry')">
          <span class="card-emoji">🧪</span>
          <h3>化学</h3>
          <p class="card-sub">从身边的化学反应到分子世界的奥秘</p>
          <span class="card-badge live">10题 · 约5分钟</span>
        </div>'''

    # Biology
    new_subject_cards += '''
        <div class="subject-select-card" onclick="startQuiz('biology')">
          <span class="card-emoji">🧬</span>
          <h3>生物</h3>
          <p class="card-sub">从微观细胞到宏观生态的生命科学</p>
          <span class="card-badge live">10题 · 约5分钟</span>
        </div>'''

    # Informatics
    new_subject_cards += '''
        <div class="subject-select-card" onclick="startQuiz('informatics')">
          <span class="card-emoji">💻</span>
          <h3>信息学</h3>
          <p class="card-sub">从图形化编程到算法竞赛</p>
          <span class="card-badge live">10题 · 约5分钟</span>
        </div>'''

    # English
    new_subject_cards += '''
        <div class="subject-select-card" onclick="startQuiz('english')">
          <span class="card-emoji">🌍</span>
          <h3>英语</h3>
          <p class="card-sub">从听说启蒙到学术英语</p>
          <span class="card-badge live">10题 · 约5分钟</span>
        </div>'''

    # History
    new_subject_cards += '''
        <div class="subject-select-card" onclick="startQuiz('history')">
          <span class="card-emoji">🏛️</span>
          <h3>历史</h3>
          <p class="card-sub">从故事到思辨，理解历史脉络</p>
          <span class="card-badge live">10题 · 约5分钟</span>
        </div>'''

    # Geography
    new_subject_cards += '''
        <div class="subject-select-card" onclick="startQuiz('geography')">
          <span class="card-emoji">🗺️</span>
          <h3>地理</h3>
          <p class="card-sub">从脚下土地到全球视野</p>
          <span class="card-badge live">10题 · 约5分钟</span>
        </div>'''

    # Politics
    new_subject_cards += '''
        <div class="subject-select-card" onclick="startQuiz('politics')">
          <span class="card-emoji">⚖️</span>
          <h3>政治</h3>
          <p class="card-sub">从身边规则到社会运行逻辑</p>
          <span class="card-badge live">10题 · 约5分钟</span>
        </div>'''

    # Insert new cards before the coming-soon cards
    # Find the last live card (chinese) and insert after it
    chinese_card_end = html.find('''        <div class="subject-select-card coming-soon">
          <span class="card-emoji">🔬</span>''')
    if chinese_card_end != -1:
        html = html[:chinese_card_end] + new_subject_cards + '\n' + html[chinese_card_end:]

    # 3. Add new RESOURCE_DATA and LEVEL_NAMES for all 7 new subjects
    # Load all resource data for the new subjects
    new_resource_entries = {}
    new_level_name_entries = {}
    new_level_desc_entries = {}

    subject_files = {
        'chemistry': 'chemistry-resources.json',
        'biology': 'biology-resources.json',
        'informatics': 'informatics-resources.json',
        'english': 'english-resources.json',
        'history': 'history-resources.json',
        'geography': 'geography-resources.json',
        'politics': 'politics-resources.json',
    }

    name_map = {"chemistry":"化学","biology":"生物","informatics":"信息学","english":"英语","history":"历史","geography":"地理","politics":"政治"}

    for sid, fname in subject_files.items():
        fpath = os.path.join(DATA_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        levels_data = {}
        level_names = {}
        level_descs = {}
        for level in data['levels']:
            lid = level['id']
            level_names[lid] = level['name']
            level_descs[lid] = f"{level['description']}，{level['ageRange']}"
            levels_data[lid] = {
                'name': level['name'],
                'description': level['description'],
                'ageRange': level['ageRange'],
                'resources': [
                    {
                        'title': r['title'],
                        'type': r['type'],
                        'description': r['description'],
                        'price': r.get('price', '')
                    }
                    for r in level.get('resources', [])[:3]
                ]
            }

        new_resource_entries[sid] = {'levels': levels_data}
        new_level_name_entries[sid] = level_names
        new_level_desc_entries[sid] = level_descs

    # Add new resource data to RESOURCE_DATA
    resource_additions_js = json.dumps(new_resource_entries, ensure_ascii=False, indent=4)
    resource_additions_js = resource_additions_js.replace('\u201c', "'").replace('\u201d', "'")

    # Add to RESOURCE_DATA - find the end of RESOURCE_DATA and add new entries
    # We'll add after the existing RESOURCE_DATA definition
    resource_add_code = f'\n    // 新增7学科资源数据\n    Object.assign(RESOURCE_DATA, {resource_additions_js});\n'

    # Find where to insert - after RESOURCE_DATA closing
    resource_data_end = html.find('    // 层级描述映射')
    if resource_data_end != -1:
        html = html[:resource_data_end] + resource_add_code + '\n' + html[resource_data_end:]

    # Add to LEVEL_NAMES
    level_names_additions_js = json.dumps(new_level_name_entries, ensure_ascii=False, indent=4)
    level_names_additions_js = level_names_additions_js.replace('\u201c', "'").replace('\u201d', "'")
    level_names_add_code = f'\n    Object.assign(LEVEL_NAMES, {level_names_additions_js});\n'

    level_names_end = html.find('    var LEVEL_EMOJIS')
    if level_names_end != -1:
        html = html[:level_names_end] + level_names_add_code + '\n' + html[level_names_end:]

    # Add to LEVEL_DESCS
    level_descs_additions_js = json.dumps(new_level_desc_entries, ensure_ascii=False, indent=4)
    level_descs_additions_js = level_descs_additions_js.replace('\u201c', "'").replace('\u201d', "'")
    level_descs_add_code = f'\n    Object.assign(LEVEL_DESCS, {level_descs_additions_js});\n'

    level_descs_end = html.find('    // ===== 状态变量 =====')
    if level_descs_end != -1:
        html = html[:level_descs_end] + level_descs_add_code + '\n' + html[level_descs_end:]

    # 4. Update the training link logic in showResult to handle all subjects
    # Replace the training link mapping
    old_link_code = """      var trainingPage = currentSubject === 'math' ? 'math-training.html' : 'chinese-training.html';"""
    new_link_code = """      var trainingPages = {'math':'math-training.html','physics':'physics-training.html','chemistry':'chemistry-training.html','biology':'biology-training.html','informatics':'informatics-training.html','chinese':'chinese-training.html','english':'english-training.html','history':'history-training.html','geography':'geography-training.html','politics':'politics-training.html'};
      var trainingPage = trainingPages[currentSubject] || 'training.html';"""
    html = html.replace(old_link_code, new_link_code)

    # 5. Update the section description
    html = html.replace(
        '<h2>选择测评学科</h2>\n        <p>每科10道题，5分钟完成，测完自动推荐对应层级资源</p>',
        '<h2>选择测评学科</h2>\n        <p>9学科可测，每科10道题，5分钟完成，测完自动推荐对应层级资源</p>'
    )

    # Update title
    html = html.replace(
        '<title>学科测评 - 非标赛道</title>',
        '<title>学科测评 - 9学科可测 - 非标赛道</title>'
    )

    return html


def update_index_html(html):
    """Update index.html with new stats."""
    # Update "3学科已上线" -> "10学科已上线"
    html = html.replace('<span class="card-count-badge">3学科已上线</span>',
                        '<span class="card-count-badge">10学科已上线</span>')

    # Update "2学科可测" -> "9学科可测"
    html = html.replace('<span class="card-count-badge">2学科可测</span>',
                        '<span class="card-count-badge">9学科可测</span>')

    # Update "数学+物理+语文训练场" description
    html = html.replace(
        '<p class="card-desc">12学科、5级进阶，每个层级都有书籍/本地/线上/名师四类精选资源</p>',
        '<p class="card-desc">10学科已上线、5级进阶，每个层级都有书籍/本地/线上/名师四类精选资源</p>'
    )

    # Update "40+精选资源" card description
    html = html.replace(
        '<p class="card-desc">数学+物理+语文训练场，每科5级×4类资源，均为真实验证</p>',
        '<p class="card-desc">10学科训练场全量上线，每科5级×4类资源，均为真实验证</p>'
    )

    # Update the "40+精选资源" title if needed
    html = html.replace(
        '<h3>40+精选资源</h3>',
        '<h3>200+精选资源</h3>'
    )

    return html


def main():
    # Read template
    template_path = os.path.join(PAGES_DIR, 'chinese-training.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_html = f.read()

    print("=== Generating 7 Training Field Pages ===")

    # Generate 7 training pages
    for subject_id, icon, filename, data_file in SUBJECTS:
        data_path = os.path.join(DATA_DIR, data_file)
        with open(data_path, 'r', encoding='utf-8') as f:
            subject_data = json.load(f)

        page_html = generate_training_page(template_html, subject_data, subject_id, icon)

        output_path = os.path.join(PAGES_DIR, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_html)

        print(f"  ✓ Created {filename}")

    print("\n=== Updating training.html ===")

    # Update training.html
    training_path = os.path.join(PAGES_DIR, 'training.html')
    with open(training_path, 'r', encoding='utf-8') as f:
        training_html = f.read()

    updated_training = update_training_html(training_html)
    with open(training_path, 'w', encoding='utf-8') as f:
        f.write(updated_training)
    print("  ✓ Updated training.html")

    print("\n=== Updating assessment.html ===")

    # Load assessment data
    assessment_path_data = os.path.join(DATA_DIR, 'assessment.json')
    with open(assessment_path_data, 'r', encoding='utf-8') as f:
        assessment_data = json.load(f)

    # Update assessment.html
    assessment_path = os.path.join(PAGES_DIR, 'assessment.html')
    with open(assessment_path, 'r', encoding='utf-8') as f:
        assessment_html = f.read()

    updated_assessment = update_assessment_html(assessment_html, assessment_data)
    with open(assessment_path, 'w', encoding='utf-8') as f:
        f.write(updated_assessment)
    print("  ✓ Updated assessment.html")

    print("\n=== Updating index.html ===")

    # Update index.html
    index_path = os.path.join(BASE_DIR, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()

    updated_index = update_index_html(index_html)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(updated_index)
    print("  ✓ Updated index.html")

    print("\n=== All done! ===")


if __name__ == '__main__':
    main()
