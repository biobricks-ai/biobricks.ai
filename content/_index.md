+++
title = "BioBricks.ai"
+++

<h2>A Bioinformatics Data Registry</h2>
Biobricks automates bioinformatics data.

**Getting Started**  
Import biobricks from [R](https://github.com/biobricks-ai/biobricks-R), [python](https://github.com/biobricks-ai/biobricks-R), or a [bash](https://github.com/biobricks-ai/biobricks):
{{< tabs >}}
{{% tab name="R" %}}
**Install biobricks**
```R
remotes::install_github("biobricks-ai/biobricks-R")
library(biobricks)
initialize()
```
**Build a brick**  
```R
# install biobricks-ai/clinvar
brick_install("clinvar")

# get data w/ _pull or _repro
brick_pull("clinvar")

# load the clinvar parquet tables
brick_load_arrow("clinvar")
```
{{% /tab %}}
{{% tab name="python" %}}
```python
# COMING SOON
```
{{% /tab %}}
{{% tab name="shell" %}}
```shell
# COMING SOON
```
{{% /tab %}}
{{< /tabs >}}

Browse the [bricks](/bricks) and example [reports](/reports).   
Become a [Github Sponsor](https://github.com/sponsors/insilica) to access private bricks and register your own.