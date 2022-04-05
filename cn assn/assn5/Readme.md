## How to Run

- In the .zip file 4 scripts are attached, data_check.py, find_whois.py, top10_ases.py, and script.sh
- in order to run the files, just run one <strong>script.sh</strong> file and please make sure you are running it in ubuntu os.
- to run script.sh file type -  
    - > ./script.sh
- if the above command does not work or it says permission denied then try running the script as follows
    - > chmod u+x script.sh
    - > ./script.sh
- running the above script.sh, will generate 6 files namely
    - a.txt - it contains the unique insti-A entires
    - top_10_ases.txt - it contains top10 ases that are connected to most of the ases
    - unique_as.txt - it contains unique ases in the file
    - unique_prefix.txt - it contains all unique prefixes ip
    - whois_data.txt - it contains the name and ases of the insti-a
    - whois_top10.txt - it contians name and ases of top10 ases

**Note** - the file may try to install whois in ubuntu since it is assumed that by default whois is not present in ubuntu

---

<style> 

table, th, td {
  border: 0.1px solid black;
  border-collapse: collapse;
}

h1,h2,h3,h4,h5,h6,p,li{
    font-family:Georgia;
}

</style>

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });
</script>