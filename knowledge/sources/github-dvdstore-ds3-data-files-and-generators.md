---
type: Source
title: ds3/data_files readmes, generator shell scripts, Install_DVDStore.pl and ds3_create_reviews.c
description: How the Small CSVs were produced (20,000 customers, 12 x 1,000 orders, 10,000 products), the review generator formula (products x 20 reviews, 2-39 helpfulness rows each) and the membership rule (10% of customers).
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/Install_DVDStore.pl
tags: [dvdstore, ds3, generator, perl, c]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/ds3_data_files_readme.txt
    title: ds3_data_files_readme.txt
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/cust/ds3_create_cust_readme.txt
    title: ds3_create_cust_readme.txt and ds3_create_cust_small.sh
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/orders/ds3_create_orders_readme.txt
    title: ds3_create_orders_readme.txt and ds3_create_orders_small.sh
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/prod/ds3_create_prod_readme.txt
    title: ds3_create_prod_readme.txt
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/Install_DVDStore.pl
    title: Install_DVDStore.pl (grep for review/member formulas)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/reviews/ds3_create_reviews.c
    title: ds3_create_reviews.c (grep)
    accessed: "2026-09-02"
---

# What was read
Readmes and shell scripts in full; the Perl installer and C generator via grep; accessed 2026-09-02.

# Relevant excerpt
* data_files readme: "The data creation programs (ds3_create_cust.c, etc.) work best when compiled and run on Linux ... due to the larger RAND_MAX. The Windows binaries ... will not provide a good degree of randomness"; "Additionally, the Small data files are included in the directories."; "Be sure to ftp, copy or unzip the data files with the appropriate settings to include the CR/LF line delimiter in DOS files but not Linux files."
* Small customers: `./ds3_create_cust 1 10000 US S 0 > us_cust.csv` and `./ds3_create_cust 10001 20000 ROW S 0 > row_cust.csv`. Small orders: twelve runs `./ds3_create_orders 1 1000 jan S 1 0 10000 20000` ... `11001 12000 dec S 12 ...` (1,000 orders per month, n_prods 10000, n_custs 20000). Products: `ds3_create_prod n_prods n_Sys_Type > prod.csv` after `ds3_create_inv n_prods n_Sys_Type > ../prod/inv.csv`; Small = 10,000 titles.
* Install_DVDStore.pl: `$par_Pct_Member = 10; # Percentage of users that are in the membership program`, `$par_Avg_Reviews = 20; # Average number of reviews per product`, `$par_review_rows = $par_n_Prod * $par_Avg_Reviews`, member rows = customers/10, `{REVIEW_HELP_ROW}` = review rows x 21; calls `ds3_create_reviews $par_n_Prod $par_Avg_Reviews $i_Cust_Rows $par_Sys_Type` and `ds3_create_membership $i_Cust_Rows $par_Pct_Member $par_Sys_Type`.
* ds3_create_reviews.c: `reviews_tot_num = n_prods * n_reviews_per_prod;` and per review `num_helpfulness_reviews = random2(3,40); for (k = 1; k < num_helpfulness_reviews; k++)` writing `review_helpfulness_id, review_id, cust_id, helpfulness_rating` (rating `random2(1,10)`); Windows output adds CR.
* Install_DVDStore.pl header: "Last updated: 10/25/21"; supports sizes up to 4096 GB; asks size, MB/GB, DB type, OS type interactively via STDIN.

# What it was used to decide
Row-count baselines and the reviews-size finding in [Dell DVD Store](/datasets/dell-dvd-store.md).
