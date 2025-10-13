# Use Ubuntu with Flutter SDK for building Android APK
FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    openjdk-11-jdk \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set up environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools
ENV FLUTTER_HOME=/opt/flutter
ENV PATH=$PATH:$FLUTTER_HOME/bin

# Install Android SDK
RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools && \
    cd $ANDROID_SDK_ROOT/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip commandlinetools-linux-9477386_latest.zip && \
    rm commandlinetools-linux-9477386_latest.zip && \
    mv cmdline-tools latest

# Accept licenses and install Android SDK packages
RUN yes | sdkmanager --licenses || true
RUN sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"

# Install Flutter
RUN git clone https://github.com/flutter/flutter.git -b stable $FLUTTER_HOME
RUN flutter precache
RUN flutter config --android-sdk $ANDROID_SDK_ROOT
RUN flutter doctor

# Set working directory
WORKDIR /app

# Copy the Flutter project
COPY src/wizard_quiz /app

# Get Flutter dependencies
RUN flutter pub get

# Build the APK
RUN flutter build apk --release

# The APK will be available at /app/build/app/outputs/flutter-apk/app-release.apk
CMD ["echo", "Build complete! APK available at: /app/build/app/outputs/flutter-apk/app-release.apk"]
