library(stargazer)
library(tidyverse)


volume_1a_col <- c(
    "Volume 112",
    "Volume 112",
    "Volume 112"
)
link_1a_col <- c(
    "https://www.aeaweb.org/issues/692",
    "https://www.aeaweb.org/issues/689",
    "https://www.aeaweb.org/issues/685"
)
issue_date_1a_col <- c(
    "September 2022 (Vol. 112, No.9 )",
    "August 2022 (Vol. 112, No.8 )",
    "July 2022 (Vol. 112, No.7 )"
)
table1a_eg_df <- data.frame(
    volume_1a_col,
    link_1a_col,
    issue_date_1a_col
)
table1a_eg_df[nrow(table1a_eg_df)+1, ] <- c("...", "...", "...")
colnames(table1a_eg_df) <- gsub("_1a_col", "", colnames(table1a_eg_df))





volume_1b_col <- c(
    "Volume 112",
    "Volume 112",
    "Volume 112",
    "Volume 112",
    "Volume 112",
    "Volume 112",
    "Volume 112"
)
issue_date_1b_col <- c(
    "September 2022 (Vol. 112, No.9 )",
    "September 2022 (Vol. 112, No.9 )",
    "September 2022 (Vol. 112, No.9 )",
    "September 2022 (Vol. 112, No.9 )",
    "September 2022 (Vol. 112, No.9 )",
    "September 2022 (Vol. 112, No.9 )",
    "September 2022 (Vol. 112, No.9 )"
)
article_title_1b_col <- c(
    "Belief Elicitation and Behavioral Incentive Compatibility",
    "Belief Elicitation and Behavioral Incentive Compatibility",
    "Dividend Taxes and the Allocation of Capital",
    "Dividend Taxes and the Allocation of Capital",
    "Dividend Taxes and the Allocation of Capital",
    "Dividend Taxes and the Allocation of Capital",
    "Dividend Taxes and the Allocation of Capital"
)
authors_1b_col <- c(
    "David Danz; Lise Vesterlund; Alistair J. Wilson",
    "David Danz; Lise Vesterlund; Alistair J. Wilson",
    "Charles Boissel; Adrien Matray",
    "Charles Boissel; Adrien Matray",
    "Charles Boissel; Adrien Matray",
    "Charles Boissel; Adrien Matray",
    "Charles Boissel; Adrien Matray"
)
page_numbers_1b_col <- c(
    "pp. 2851-83",
    "pp. 2851-83",
    "pp. 2884-2920",
    "pp. 2884-2920",
    "pp. 2884-2920",
    "pp. 2884-2920",
    "pp. 2884-2920"
)
article_link_1b_col <- c(
    "https://doi.org/10.1257/ aer.20201248",
    "https://doi.org/10.1257/ aer.20201248",
    "https://doi.org/10.1257/ aer.20210369",
    "https://doi.org/10.1257/ aer.20210369",
    "https://doi.org/10.1257/ aer.20210369",
    "https://doi.org/10.1257/ aer.20210369",
    "https://doi.org/10.1257/ aer.20210369"
)
jel_code_1b_col <- c(
    "D83",
    "D91",
    "D22",
    "G31",
    "G35",
    "H25",
    "H32"
)
jel_description_1b_col <- c(
    "Search; Learning; Information and Knowledge; Communication; Belief; Unawareness",
    "Micro-Based Behavioral Economics: Role and Effects of Psychological, Emotional, Social, and Cognitive Factors on Decision Making",
    "Firm Behavior: Empirical Analysis",
    "Capital Budgeting; Fixed Investment and Inventory Studies; Capacity",
    "Payout Policy",
    "Business Taxes and Subsidies including sales and value-added (VAT)",
    "Fiscal Policies and Behavior of Economic Agents: Firm"
)

table1b_eg_df <- data.frame(
    volume_1b_col,
    issue_date_1b_col,
    article_title_1b_col,
    authors_1b_col,
    page_numbers_1b_col,
    article_link_1b_col,
    jel_code_1b_col,
    jel_description_1b_col
)

table1b_eg_df[nrow(table1b_eg_df) + 1, ] <- c("...", "...", "...", "...", "...", "...", "...", "...")
colnames(table1b_eg_df) <- gsub("_1b_col", "", colnames(table1b_eg_df))

#### Table column alignment should be modified from
# ccc
# to
# lll
stargazer(
    table1a_eg_df,
    title = "Example Task 1A Output Structure",
    out = "table1a_eg.tex",
    summary = FALSE,
    rownames = FALSE,
    style = "aer"
)


#### Table column alignment should be modified from
# cccccccc
# to
# l<{\raggedright}p{0.075\linewidth}<{\raggedright}p{0.11\linewidth}<{\raggedright}p{0.11\linewidth}l<{\raggedright}p{0.15\linewidth}<{\raggedright}l<{\raggedright}p{0.16\linewidth}
stargazer(
    table1b_eg_df,
    title = "Example Task 1B Output Structure",
    out = "table1b_eg.tex",
    summary = FALSE,
    rownames = FALSE,
    font.size = "footnotesize",
    style = "aer"
)
