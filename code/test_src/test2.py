def cal(b,m,c,w,d,t):
    #(0.541316 (d + t) (36 + 36 c + 36 (1 + b + c) + 36 m + 120 (1 + b + c) (1 + c + m) + 2 t + b t + 2 c t + m t) (t + w))/((1 + b + c) (1 + c + m) t (120 (d + t + w) + ((36 + t) (t + w) + d (36 + t + w))/(1 + b + c) + ((36 + t) (t + w) + d (36 + t + w))/(1 + c + m)))
    value = (0.541316 * (d + t) * (36 + 36 * c + 36 * (1 + b + c) + 36 * m + 120 * (1 + b + c) * (1 + c + m) + 2 * t + b * t + 2 * c * t + m * t) * (t + w))/((1 + b + c) * (1 + c + m) * t * (120 * (d + t + w) + ((36 + t) * (t + w) + d * (36 + t + w))/(1 + b + c) + ((36 + t) * (t + w) + d * (36 + t + w))/(1 + c + m)))
    return value

valueList = []
