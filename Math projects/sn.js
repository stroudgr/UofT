function sum(a) {
  var sum = 0;
  for (var i = 0; i < a.length; i++)
    sum += a[i];
  return sum;
}

// Returns the "largest" cycle_type with a k-cycle in it from Sn.
function start(k, n){
    // Assume k <= n
    var out = [];
    var sums = sum(out);

    // Output is basically just [k,...,k, k%n]
    while (sums != n) {
        out.push(k);
        sums = sums + k;
        if (sums + k > n) {
          if (n-sums != 0) {
            out.push(n-sums);
          }
          return out;
        }
    }
    return out;
}

// Given a cycle of type x, returns the next smallest element in iteration.
function next_element(x, n) {

    // Find first index that is not 1.
    var l = x.length - 1;
    while (l != 0 && x[l] == 1) {
        l -= 1;
    }

    // Reached the end.
    if (l == 0 && x[0] == 1) {
        return null;
    }

    // Special case when the first element changes from x to successor.
    // Use a helper function.
    if (l == 0 && x[0] > 0) {
        return start(x[l] - 1, n);
    }

    var out = x.slice();
    out[l] -= 1;

    // Takes the 1 and puts it at the end; e.g. (6,2,1) --> (6,2,1,1)
    if (out[l] == 1 || l == x.length - 1) {
        out.push(1)
    }
    // Otherwise adds the one the the adjacent location; e.g. (6,4,1) --> (6,3,2)
    else
        out[l+1] += 1;
    return out;
}

// Returns all the cycle types of Sn.
function cycle_types(n) {

    var l = [[n]];
    var z = next_element([n], n);
    while (z != null) {
        l.push(z);
        z = next_element(z, n);
    }
    return l;
}

function lcm(a) {
    var l = a[0];
    for (var i = 1; i < a.length; i++) {
        l = l*Math.floor(a[i]/gcd(l, a[i]));
    }
    return l;
}

function gcd_alt(a,b) {
    var r,i;
    while(b != 0) {
        r = a % b;
        a = b;
        b = r;
    }
    return a;
  }

  function gcd(a,b) {
      a = Math.abs(a)
      b = Math.abs(b)
      return (b == 0) ? a : gcd(b, a%b);
    }

function choose(n, k) {
    return Math.floor(fact(n)/(fact(n-k)*fact(k)));
}

var f = {};

function fact(k) {
    if (k <= 0 || k == null)
        return 1;
    if (k in f)
        return f[k];
    f[k] = k*fact(k-1);
    return f[k];
}

// Returns the number of elements of the cycle_type.
function number_of_elements(cycle_type, n) {
    var d = {};

    var out = 1;

    var left = n;

    for (var z = 0; z < cycle_type.length; z++) {
        var x = cycle_type[z];

        if (!(x in d))
            d[x] = 1;
        else
            d[x] += 1;

        out *= fact(x-1)*choose(left, x);
        left -= x;
    }
    for (x in d)
        out = out / fact(d[x]);

    return out;
}

var ds = {};
var outputs = {};

// Returns an html table of the cycle type, its order and number of elements of this cycle type.
function sn(n=null) {

    if (n == null) {
      n = parseInt(document.getElementById("myText").value);
    }
    if (n == NaN || !(n > 0) || n == null) {
      return "<tr><th>Cycle types</th><th>order</th><th>Number of elements of this order</th></tr>";;
    }

    if (n in outputs) {
      return outputs[n];
    }


    var d = {};
    var c = cycle_types(n);

    for (var i = 0; i < c.length; i++) {
        var y = c[i];
        d[y] = [lcm(y).toString(), number_of_elements(y, n).toString()];
    }
    var html = "";
    html += "<tr><th>Cycle types</th><th>order</th><th>Number of elements of this order</th></tr>";

    for (fruit in d) {
        html += "<tr><td>" + fruit.toString() + "</td>";
        html += "<td>" + d[fruit][0] + "</td>";
        html += "<td>" + d[fruit][1] + "</td>";
        html += "</tr>"
    }

    ds[n] = d;
    outputs[n] = html;
    return html;
}

// Returns an html table of order, and number of elements of the order.
function sn2() {
  var n = parseInt(document.getElementById("myText").value);
  if (n == NaN || !(n > 0) || n == null) {
    return "<tr><th>Cycle types</th><th>order</th><th>Number of elements of this order</th></tr>";;
  }

  if (!(n in ds)) {
    sn();
  }

  var d = ds[n];
  var orders = {};

  for (x in d) {

    var order = d[x][0];
    var count = d[x][1];

    if (!(order in orders)) {
      orders[order] = parseInt(count);
    }
    else {
      orders[order] += parseInt(count);
    }
  }

  var html = "";
  html += "<tr><th>Order</th><th>Number of elements of this order</th></tr>";

  for (fruit in orders) {
      html += "<tr><td>" + fruit.toString() + "</td>";
      html += "<td>" + orders[fruit].toString() + "</td>";
      html += "</tr>"
  }

  return html;
}
