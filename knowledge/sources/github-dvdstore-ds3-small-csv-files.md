---
type: Source
title: DS3 Small CSV data files (inspection, 2026-09-02)
description: Sizes, line counts, encoding and sample rows of the committed Small data set, including the 200,000-row reviews and 4,106,382-row review_helpfulness files.
resource: https://github.com/dvdstore/ds3/tree/master/ds3/data_files
tags: [dvdstore, ds3, csv, measurement]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.github.com/repos/dvdstore/ds3/git/trees/HEAD?recursive=1
    title: repository tree with blob sizes
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/cust/us_cust.csv
    title: us_cust.csv, row_cust.csv, prod/prod.csv, prod/inv.csv, membership/membership.csv, orders/*_orders.csv, *_orderlines.csv, *_cust_hist.csv (fetched and counted)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/reviews/reviews.csv
    title: reviews.csv and review_helpfulness.csv (HEAD + HTTP Range on head and tail only)
    accessed: 2026-09-02
---

# What was read
Blob sizes from the git tree; the small files were fetched and measured with `wc -l`, `grep -cP '[^\x00-\x7F]'`, `grep -c $'\r'`; the two large review files were only probed with HEAD and Range requests (first 800 bytes, last 6,000 bytes).

# Relevant excerpt (measurements)
| file | bytes | rows | notes |
|---|---|---|---|
| cust/us_cust.csv | 1,529,725 | 10,000 | customerid 1-10000, COUNTRY US |
| cust/row_cust.csv | 1,574,627 | 10,000 | customerid 10001-20000, e.g. UK, ZIP `00000` |
| prod/prod.csv | 510,392 | 10,000 | `1,14,ACADEMY ACADEMY,PENELOPE GUINESS,25.99,0,1976,1` |
| prod/inv.csv | 113,269 | 10,000 | `1,138,9` |
| membership/membership.csv | 36,889 | 2,000 | `1,2,2019/08/15` ... last `19995,3,2019/04/15` |
| orders/{jan..dec}_orders.csv | 39,459-41,673 each | 1,000 each = 12,000 | `1,2013/01/27,7888,313.24,25.84,339.08` |
| orders/{mon}_orderlines.csv | 120,882-129,224 each | 60,350 total | `1,1,9117,1,2013/01/27` |
| orders/{mon}_cust_hist.csv | 72,206-81,422 each | 60,350 total | `7888,1,9117` |
| reviews/reviews.csv | 101,366,769 | 200,000 (last id 200000) | `1,8402,2013/05/25,4,18233,Cut Captain purchased,join insight ...` (REVIEW_TEXT up to 1000 chars of random words) |
| reviews/review_helpfulness.csv | 89,190,629 | 4,106,382 (last id) | `4106382,200000,11273,9` |

* All sampled files: no header row, LF line endings (0 CR bytes), pure ASCII (0 non-ASCII lines). Dates are `YYYY/MM/DD`; card expiry `YYYY/MM`; passwords are the literal `password`; credit-card numbers are synthetic 16-digit strings; e-mails `<LASTNAME>@dell.com`; customer names are random uppercase letter strings (`VKUUXF ITHOMQJNYX`).
* Orderline rows per order month vary (4,942-5,164), i.e. about 5 lines per order.

# What it was used to decide
Row-count baselines, encoding statement and the core/extended split in [Dell DVD Store](/datasets/dell-dvd-store.md).
