"""
Team 8 - Shadowfax

Mohammed Tawfik Sadhik Batcha
Huzaifa Mehmood
Karthikaijothi Murugan
Thamjeed Abdulla Kuniyil

"""

# Updated portrait merging logic for efficiency
def merge_portraits(portrait_tags, batch_size=800):
    portrait_tags = dict(sorted(portrait_tags.items(), key=lambda x: len(x[1]), reverse=True))
    
    portrait_indexes = list(portrait_tags.keys())
    merged_portraits = []
    
    for i in range(0, len(portrait_indexes), batch_size):
        batch = portrait_indexes[i:i+batch_size]
        used = set()

        for i, first in enumerate(batch):
            if first in used:
                continue
            best_pair = None
            best_common_tags = float('inf')
            used.add(first)
            
            for second in batch:
                if second in used:
                    continue
                common_tags = len(portrait_tags[first].intersection(portrait_tags[second]))
                if common_tags < best_common_tags:
                    best_pair = second
                    best_common_tags = common_tags

            if best_pair:
                merged_tags = list(portrait_tags[first].union(portrait_tags[best_pair]))
                merged_portraits.append({
                    'type': 'P',
                    'paintings': [first, best_pair],
                    'tags': merged_tags
                })
                used.add(best_pair)

    return merged_portraits

# Batch-based sorting optimization
def process_paintings(file_path, is_binary=False):
    landscape_tags = {}
    portrait_tags = {}
    tag_frameglasses = {}
    with open(file_path, 'r') as file:
        n = int(next(file).strip())
        frameglasses = []
        for i in range(n):
            line = next(file).strip().split()
            painting_type = line[0]
            tags = set(line[2:int(line[1])+2])
            if painting_type == 'L':
                landscape_tags[i] = tags
                frameglasses.append({'type': 'L', 'paintings': [i], 'tags': list(tags)})
            elif painting_type == 'P':
                portrait_tags[i] = tags
            for tag in tags:
                tag_frameglasses.setdefault(tag, []).append(i)

        merged_portraits = merge_portraits(portrait_tags, 2000)
        frameglasses.extend(merged_portraits)
        if is_binary:
            return frameglasses, landscape_tags, portrait_tags, tag_frameglasses
        frameglasses.sort(key=lambda x: len(x['tags']), reverse=True)
    return frameglasses, landscape_tags, portrait_tags, tag_frameglasses

# Satisfaction calculation remains intact
def get_robotic_satisfaction(frameglass1, frameglass2):
    common_tags = len(set(frameglass1['tags']).intersection(set(frameglass2['tags'])))
    tags_in_frameglass1 = len(set(frameglass1['tags']).difference(set(frameglass2['tags'])))
    tags_in_frameglass2 = len(set(frameglass2['tags']).difference(set(frameglass1['tags'])))
    return min(common_tags, tags_in_frameglass1, tags_in_frameglass2)

# Optimized batch satisfaction calculation
def get_max_satisfaction_batch(frameglass_combos, chunk_size=100):
    if not frameglass_combos:
        return 0, []
    curr_fg = frameglass_combos[0]
    res = [curr_fg]
    rem_fg = frameglass_combos[1:]
    total_satisfaction = 0
    while rem_fg:
        max_satisfaction = -1
        max_fg = None
        for i in range(min(chunk_size, len(rem_fg))):
            satisfaction = get_robotic_satisfaction(curr_fg, rem_fg[i])
            if satisfaction > max_satisfaction:
                max_satisfaction = satisfaction
                max_fg = rem_fg[i]
        if max_fg:
            res.append(max_fg)
            rem_fg.remove(max_fg)
            total_satisfaction += max_satisfaction
            curr_fg = max_fg
        else:
            break
    for i in range(0, len(rem_fg), 2):
        total_satisfaction += get_robotic_satisfaction(rem_fg[i], rem_fg[i+1])
        res.append(rem_fg[i])
        res.append(rem_fg[i+1])
    return total_satisfaction, res

# Binary case logic updated
def best_combo_binary(frameglasses, tag_frameglasses):
    best_combo = []
    fg_copy = frameglasses.copy()
    frameglasses = sort_frameglasses_by_frequency(frameglasses)
    max_satisfaction = 0
    visited = set()
    best_combo.append(frameglasses[0])
    visited.add(frameglasses[0]['paintings'][0])
    frameglasses.pop(0)
    while frameglasses:
        curr = best_combo[-1]
        neighbors = []
        for tag in curr['tags']:
            neighbors.extend([index for index in tag_frameglasses[tag] if index not in visited])
        for neighbor in neighbors:
            if neighbor not in visited:
                nb_common_tags = len(set(curr['tags']).intersection(set(fg_copy[neighbor]['tags'])))
                nb_tags = len(fg_copy[neighbor]['tags'])
                if nb_tags >= 2 * nb_common_tags:
                    best_combo.append(fg_copy[neighbor])
                    visited.add(neighbor)
                    frameglasses.remove(fg_copy[neighbor])
                    break
        if not neighbors:
            best_combo.append(frameglasses[0])
            visited.add(frameglasses[0]['paintings'][0])
            frameglasses.pop(0)
            curr = best_combo[-1]
    for i in range(len(best_combo) - 1):
        max_satisfaction += get_robotic_satisfaction(best_combo[i], best_combo[i+1])
    return max_satisfaction, best_combo

# Write output logic intact
def write_output_file(output_file_path, best_combo):
    with open(output_file_path, 'w') as file:
        file.write(str(len(best_combo)) + '\n')
        for frameglass in best_combo:
            if frameglass['type'] == 'L':
                file.write(str(frameglass['paintings'][0]) + '\n')
            elif frameglass['type'] == 'P':
                file.write(str(frameglass['paintings'][0]) + ' ' + str(frameglass['paintings'][1]) + '\n')

# sort by frequency of number of tags
def sort_frameglasses_by_frequency(frameglasses):
    frequency = {}
    for frameglass in frameglasses:
        num_tags = len(frameglass['tags'])
        if num_tags not in frequency:
            frequency[num_tags] = []
        frequency[num_tags].append(frameglass)
    
    sorted_frameglasses = []
    for num_tags in sorted(frequency.keys(), reverse=True):
        sorted_frameglasses.extend(frequency[num_tags])

    sorted_frameglasses.reverse()
    
    return sorted_frameglasses


# Main logic with conditional handling
def main(input_file_path, is_binary=False, is_oily=False, is_random=False, is_computable=False, is_example=False):
    input_file_path = 'Data/' + input_file_path
    paintings, landscape_tags, portrait_tags, tag_frameglasses = process_paintings(input_file_path, is_binary=is_binary)
    max_satisfaction = 0
    max_satisfaction_combo = []
    if is_example:
        max_satisfaction, max_satisfaction_combo = get_max_satisfaction_batch(paintings, 10)
    if is_computable:
        max_satisfaction, max_satisfaction_combo = get_max_satisfaction_batch(paintings, 1000)
    if is_binary:
        max_satisfaction, max_satisfaction_combo = best_combo_binary(paintings, tag_frameglasses)
        return max_satisfaction
    if is_oily:
        max_satisfaction, max_satisfaction_combo = get_max_satisfaction_batch(paintings, 1000)
        max_satisfaction, max_satisfaction_combo = get_max_satisfaction_batch(max_satisfaction_combo, 2000)
    if is_random:
        max_satisfaction, max_satisfaction_combo = get_max_satisfaction_batch(paintings, 600)
        max_satisfaction, max_satisfaction_combo = get_max_satisfaction_batch(max_satisfaction_combo, 1500)
    output_file_path = 'Output/' + str(max_satisfaction) + '-' + input_file_path.split('/')[-1].replace('.txt', '_output.txt')
    write_output_file(output_file_path, max_satisfaction_combo)
    
    return max_satisfaction


