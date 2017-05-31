def list_numbers(nums):
    final_arr = []
    arr = nums.split(',')
    for thing in arr:
        if "-" not in thing:
            final_arr.append(int(thing) - 1)
        else:
            t = thing.split("-")
            for i in range(int(t[0]), int(t[1]) + 1):
                final_arr.append(int(i) - 1)
    return final_arr
