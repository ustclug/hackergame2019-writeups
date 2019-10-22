var now = new Date("2078").toUTCString();
var ua = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) HEICORE/49.1.2623.213 Safari/537.36";
$http.post({
  url: "http://202.38.93.241:2077/flag.txt",
  header: { "If-Unmodified-Since": now, "User-Agent": ua },
  handler: function(resp) {
    console.log(resp.data);
  }
});