<?php
/**
 * jvasak: minimal block theme. Server-side helpers only, no front-end JavaScript.
 */

add_action( 'after_setup_theme', function () {
	register_nav_menus( array( 'primary' => __( 'Primary menu', 'jvasak' ) ) );
	add_editor_style( 'style.css' );
} );

add_action( 'init', function () {
	register_block_style( 'core/button', array( 'name' => 'secondary', 'label' => __( 'Secondary', 'jvasak' ) ) );
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
} );

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'jvasak', get_stylesheet_uri(), array(), wp_get_theme()->get( 'Version' ) );
} );

// Preload the font files used above the fold. Every page needs the latin-ext files too
// ("Vašák" in the header and footer, Czech text), and the browser only finds them after the CSS.
add_action( 'wp_head', function () {
	foreach ( array( 'spectral-normal-latin', 'spectral-normal-latin-ext', 'dm-sans-normal-latin', 'dm-sans-normal-latin-ext' ) as $font ) {
		printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( get_theme_file_uri( "assets/fonts/$font.woff2" ) ) );
	}
}, 1 );

// Polylang free does not filter Query Loop blocks by language; do it here.
add_filter( 'query_loop_block_query_vars', function ( $query ) {
	if ( function_exists( 'pll_current_language' ) && empty( $query['lang'] ) ) {
		$query['lang'] = pll_current_language();
	}
	return $query;
} );

// No duplicate ids: the menu is printed twice (wide and narrow screens).
add_filter( 'nav_menu_item_id', '__return_empty_string' );

function jvasak_lang() {
	return function_exists( 'pll_current_language' ) ? pll_current_language() : 'en';
}

// [jv_menu]: classic "primary" menu (Polylang free assigns it per language); <details> toggle on small screens.
add_shortcode( 'jv_menu', function () {
	$args = array( 'theme_location' => 'primary', 'container' => false, 'menu_class' => 'jv-menu', 'items_wrap' => '<ul class="%2$s">%3$s</ul>', 'depth' => 1, 'fallback_cb' => false, 'echo' => false );
	$menu = wp_nav_menu( $args );
	if ( ! $menu ) {
		return '';
	}
	return '<nav class="jv-nav" aria-label="' . esc_attr__( 'Main' ) . '">' . $menu
		. '<details class="jv-nav-mobile"><summary>' . esc_html__( 'Menu' ) . '</summary>' . $menu . '</details></nav>';
} );

// [year], [jv_t en="…" cs="…"], [jv_home_url], [jv_page_title] for template text that differs per language.
add_shortcode( 'year', fn() => esc_html( wp_date( 'Y' ) ) );
add_shortcode( 'jv_t', fn( $atts ) => esc_html( $atts[ jvasak_lang() ] ?? $atts['en'] ?? '' ) );
add_shortcode( 'jv_home_url', fn() => esc_url( function_exists( 'pll_home_url' ) ? pll_home_url() : home_url( '/' ) ) );
add_shortcode( 'jv_page_title', fn() => esc_html( single_post_title( '', false ) ) );
