# Require any additional compass plugins here.
# add_import_path "./genweb/theme/bootstrap/scss"
additional_import_paths = [
"./genweb/upc/bootstrap/scss",
"../genweb.alternatheme/genweb/alternatheme/components",]

# Set this to the root of your project when deployed:
http_path = "/"
css_dir = "./genweb/upc/stylesheets"
sass_dir = "./genweb/upc/scss"
http_images_path = "++genweb++static/images"
images_dir = "../genweb.core/genweb/core/static/images"
javascripts_dir = "./genweb/upc/bootstrap/js"

# You can select your preferred output style here (can be overridden via the command line):
# output_style = :expanded or :nested or :compact or :compressed
# output_style = :compressed

# To enable relative paths to assets via compass helper functions. Uncomment:
#relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
# line_comments = false


# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass ./bootstrap/scss scss && rm -rf sass && mv scss sass
