for i in range(71, 72):
    # 读取原始txt文件
    # start = i - 2
    start = i * 1000
    with open(f'./Figurewebofsciencedown/savedrecs ({i}).txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # 分割内容块
    content_blocks = content.split('\n\n')

    # 准备一个字典来存储处理后的TI和AB内容
    processed_contents = {}

    # 对每个内容块进行处理
    for block in content_blocks:
        lines = block.split('\n')
        ti_content = []
        ab_content = []
        capturing_ti = False
        capturing_ab = False

        # 逐行检查并处理
        for line in lines:
            if line.startswith('TI'):
                capturing_ti = True
                ti_content.append(line.strip())
            elif line.startswith('AB'):
                capturing_ab = True
                capturing_ti = False
                ab_content.append(line.strip())
            elif line.startswith('PT') or line.startswith('AU') or line.startswith('DA') or line.startswith(
                    'UT') or line.startswith('PM') or line.startswith('ER') or line.startswith('EA'):
                capturing_ti = False
                capturing_ab = False
            elif capturing_ti:
                ti_content.append(line.strip())
            elif capturing_ab:
                ab_content.append(line.strip())

        # 将TI和AB的内容合并为一行，并存储到字典中
        if ti_content or ab_content:
            processed_contents[len(processed_contents) + 1] = [' '.join(ti_content), ' '.join(ab_content)]

    # 将处理后的内容写入新的txt文件
    for idx, (ti, ab) in processed_contents.items():
        with open(f'./Figuretext/{str(int(idx) + start)}.txt', 'w', encoding='utf-8') as file:
            file.write(ti + '\n')
            file.write(ab + '\n')
