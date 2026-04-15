# Configuration for latexmk to handle bibliographies and glossaries
# Run makeglossaries if necessary
add_cus_dep('glo', 'gls', 0, 'makeglossaries');
add_cus_dep('acn', 'acr', 0, 'makeglossaries');

sub makeglossaries {
    if ( $silent ) {
        system( "makeglossaries -q \"$_[0]\"" );
    }
    else {
        system( "makeglossaries \"$_[0]\"" );
    };
}

# Always try to run bibtex if citations are found
$bibtex_use = 2;
