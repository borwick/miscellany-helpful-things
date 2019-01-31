// Nov 2006 by John Borwick
//
// ==UserScript==
// @name          Amazon Registry Compact Table Titles
// @namespace     http://www.johnborwick.com
// @description   remove all compact items info except title/author
// @include       http://www.amazon.com/gp/registry/wishlist*
// ==/UserScript==


// my first XPath command evah!
var compactTables = document.evaluate(
"//table[@class='compact-items']",
    document,
    null,
    XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
    null);

compactTable = compactTables.snapshotItem( 0 );


if ( compactTable ) {
  // now that you've found the table, get the rows:
  allRows = compactTable.getElementsByTagName( 'tr' );

  for ( var tr_index=0;
        tr_index < allRows.length;
        tr_index++ ) {
    curRow = allRows[tr_index];
    for ( var td_index= curRow.cells.length -1;
          td_index >= 0;
          td_index-- ) {
      GM_log( "iterating, td_index=" + td_index );
      if ( td_index != 1 ) {
        GM_log( "deleteCell " + td_index );
        curRow.deleteCell( td_index );
      }
    }
  }
}
