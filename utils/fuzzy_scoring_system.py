class FuzzyScoringSystem:
    def __init__(self, count, main_threshold_lower, main_threshold_upper, soft_threshold_lower, soft_threshold_upper) -> None:
        self.count = count
        
        # Thresholds for scoring 1
        self.main_threshold_lower = main_threshold_lower
        self.main_threshold_upper = main_threshold_upper
        
        # Thresholds for scoring between 0 and 1
        self.soft_threshold_lower = soft_threshold_lower
        self.soft_threshold_upper = soft_threshold_upper
        
    def score(self):
        if self.soft_threshold_lower <= self.count < self.main_threshold_lower:
            return ((self.count - self.soft_threshold_lower)/(self.main_threshold_lower - self.soft_threshold_lower))
        if self.main_threshold_lower <= self.count <= self.main_threshold_upper:
            return 1.0
        if self.main_threshold_upper < self.count <= self.soft_threshold_upper:
            return abs((self.count - self.soft_threshold_upper)/(self.main_threshold_upper - self.soft_threshold_upper))
        return 0.0