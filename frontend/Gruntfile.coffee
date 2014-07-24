project = {
    src: 'src/'
    test: 'test/'
    dist: 'dist/'
    styles: 'styles/'
}


module.exports = (grunt) ->
    # Load grunt tasks automatically
    require('load-grunt-tasks')(grunt)

    # Time how long tasks take. Can help when optimizing build times
    require('time-grunt')(grunt)

    # Config
    grunt.initConfig
        # Project settings
        project: project

        bwr: grunt.file.readJSON('bower.json')

        # слежение за изменением файлов
        watch:
            gruntfile:
                files: ['Gruntfile.coffee']
            scss:
                files: ['<%= project.styles %>/*.scss']
                tasks: ['sass:src']
            src:
                files: ['<%= project.src %>/**/*.js']
            conf:
                files: ['<%= project.src %>/config/environments/*.json']
                tasks: ['replace:dev']

            # restart web-server when files refreshed
#            livereload:
#                options:
#                    livereload: '<%= connect.options.livereload %>'
#                files: [
#                    '*.html',
#                    '<%= project.styles %>/*.css',
#                    '<%= project.src %>/**/*.js',
#                    '<%= project.src %>/**/*.html',
#                    '**/*.{png,jpg,jpeg,gif,webp,svg}'
#                ]


        # Grunt server settings
        connect:
            options:
                port: 8001
                hostname: 'localhost'
                livereload: 35724
            dev:
                options:
                    open: true
            dist:
                options:
                    open: true
                    base: [
                        '<%= project.dist %>'
                    ]

        # Compiles CoffeeScript to JavaScript
        coffee:
            dist:
                options:
                    sourceMap: true
                files: [{
                    expand: true
                    cwd: '<%= project.src %>'
                    src: '**/*.coffee'
                    dest: '<%= project.dist %>/src'
                    ext: '.js'
                }]
            src:
                files: [{
                    expand: true
                    cwd: '<%= project.src %>'
                    src: '**/*.coffee'
                    dest: '<%= project.src %>'
                    ext: '.js'
                }]
            test:
                files: [{
                    expand: true
                    cwd: '<%= project.test %>'
                    src: '**/*.spec.coffee'
                    dest: '<%= project.test %>'
                    ext: '.spec.js'
                }]

        # Compiles Sass to CSS
        sass:
            dist:
                files: [{
                    expand: true
                    cwd: '<%= project.styles %>'
                    src: '**/*.scss'
                    dest: '<%= project.dist %>/styles'
                    ext: '.css'
                }]
            src:
                files: [{
                    expand: true
                    cwd: '<%= project.styles %>'
                    src: '**/*.scss'
                    dest: '<%= project.styles %>'
                    ext: '.css'
                }]


        replace:
            # prepare config
            dev:
                options:
                    patterns: [{
                        json: grunt.file.readJSON(project.src + 'config/environments/development.json')
                    }]
                files: [{
                    flatten: true,
                    expand: true,
                    cwd: '<%= project.src %>'
                    src: 'config/config.js'
                    dest: '<%= project.src %>/app/'
                }]
            prod:
                options:
                    patterns: [{
                        json: grunt.file.readJSON(project.src + 'config/environments/production.json')
                    }]
                files: [{
                    flatten: true,
                    expand: true,
                    cwd: '<%= project.src %>'
                    src: 'config/config.js'
                    dest: '<%= project.src %>/app/'
                    }]

            test:
                options:
                    patterns: [{
                        json: grunt.file.readJSON(project.src + 'config/environments/development.json')
                    }]
                src: '<%= project.src %>/config/config.tpl.js'
                dest: '<%= project.test %>/tmp/config.js'




        clean:
            pre_dist:
                files: [{
                    dot: true,
                    src: [
                        '<%= project.dist %>/*'
                        '.sass-cache'
                        '.tmp'
                    ]
                }]
            post_dist:
                files: [{
                    dot: true,
                    src: [
                        '.sass-cache'
                        '.tmp'
                    ]
                }]
            test:
                src: '<%= project.test %>/tmp/'

        copy:
            dist:
                files: [
                    {
                        expand: true,
                        cwd: '<%= project.src %>'
                        dest: '<%= project.dist %>/src'
                        src: [
                            '**/*.coffee'
                            '**/*.html'
                        ]
                    }, {
                        expand: true,
                        cwd: 'bower_components/ionic/fonts/'
                        src: '*'
                        dest: '<%= project.dist %>/fonts'
                    }
                ]
            build_unuglified_app:
                files: [{
                    src: '.tmp/concat/scripts/app.js'
                    dest: '<%= project.dist %>/scripts/app.js'
                }]


        useminPrepare:
            dist:
                src: '*.html'
            test:
                src: '*.html'
                options:
                    staging: '<%= project.test %>/tmp'

        # Performs rewrites based on rev and the useminPrepare configuration
        usemin:
            html: ['<%= project.dist %>/*.html']
            css: ['<%= project.dist %>/styles/{,*/}*.css'],
            options: {
                dirs: ['<%= project.dist %>']
                basedir: ['<%= project.dist %>']
            }

        ngmin:
            dist:
                files: [
                    {
                        src: '.tmp/concat/scripts/app.js'
                        dest: '.tmp/concat/scripts/app.js'
                    }
                ]

        htmlmin:
            dist:
                files: [{
                    expand: true,
                    cwd: '.'
                    src: ['*.html']
                    dest: '<%= project.dist %>'
                }]

        # Renames files for browser caching purposes
        rev:
            dist:
                files:
                    src: [
                        '<%= project.dist %>/scripts/*.js'
                        '<%= project.dist %>/styles/*.css'
                    ]


        # Make sure code styles are up to par and there are no obvious mistakes
        coffeelint:
            options:
                indentation:
                    value: 4
                    level: "warn"
                max_line_length:
                    value: 120
                    level: "warn"
            app: [
                '<%= project.src %>/**/*.coffee'
            ]
            test: [
                '<%= project.test %>/**/*.coffee'
            ]

        # Test settings
        karma:
            unit:
                configFile: '<%= project.test %>/config/karma-unit.conf.js'
                singleRun: true
            teamcity:
                configFile: '<%= project.test %>/config/karma-unit.conf.js'
                singleRun: true
                reporters: 'teamcity'


    grunt.registerTask 'serve', [
        'replace:dev'
        'coffee:src'
        'sass:src'
        'connect:dev'
        'watch'
    ]

    grunt.registerTask 'serve_dist', [
        'connect:dist'
        'watch'
    ]


    grunt.registerTask 'test', [
        'clean:test'
        'coffeelint'
        'coffee:src'
        'replace:test'

        'useminPrepare:test'
        'concat:generated'

        'coffee:test'
        'karma:unit'

        'clean:test'
    ]

    grunt.registerTask 'build', (target) ->
        if not target
            target = 'prod'

        grunt.task.run([
            'clean:pre_dist'
            'copy:dist'
            'coffee:dist'
            'sass:src'
            'sass:dist'
            'replace:' + target

            'useminPrepare:dist'
            'htmlmin'
            'concat'
            'cssmin'
            'ngmin'
            'uglify:generated'
            'copy:build_unuglified_app'
            'rev:dist'
            'usemin'

            'clean:post_dist'
        ]);
