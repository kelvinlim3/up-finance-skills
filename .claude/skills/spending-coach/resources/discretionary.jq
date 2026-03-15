def non_discretionary_categories: [
  "rent-and-mortgage", "utilities", "home-insurance-and-rates",
  "health-and-medical", "education-and-student-loans", "family",
  "car-insurance-and-maintenance", "car-repayments"
];

def is_transfer: .description | test(
  "^(Transfer (from|to)|Cover (from|to)|Forward (from|to)|Auto Transfer (from|to)|Quick save transfer (from|to)|Round Up|Final interest payment from)";
  "i"
);

[.[] | select(
  (is_transfer | not)
  and ((.amount | tonumber) < 0)
  and ((.category // "") | IN(non_discretionary_categories[]) | not)
)]
| {
    total: (map(.amount | tonumber) | add | fabs | . * 100 | round | . / 100),
    count: length,
    by_category: (
      group_by(.category)
      | map({
          category: (.[0].category // "uncategorised"),
          total: (map(.amount | tonumber) | add | fabs | . * 100 | round | . / 100),
          count: length,
          topMerchants: (group_by(.description) | sort_by(-length) | .[0:3] | map(.[0].description))
        })
      | sort_by(.total) | reverse | .[0:8]
    )
  }
