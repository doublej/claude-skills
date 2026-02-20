import SwiftUI

// MARK: - App Entry Point
@main
struct ExampleApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
  }
}

// MARK: - Main Content View
struct ContentView: View {
  @State private var selectedTab = 0

  var body: some View {
    TabView(selection: $selectedTab) {
      HomeView()
        .tabItem {
          Label(String(localized: "tab.home"), systemImage: "house.fill")
        }
        .tag(0)

      ExploreView()
        .tabItem {
          Label(String(localized: "tab.explore"), systemImage: "magnifyingglass")
        }
        .tag(1)

      ProfileView()
        .tabItem {
          Label(String(localized: "tab.profile"), systemImage: "person.fill")
        }
        .tag(2)
    }
  }
}

// MARK: - Home Screen
struct HomeView: View {
  @State private var items: [Item] = []
  @State private var isLoading = true

  var body: some View {
    NavigationStack {
      ZStack {
        // Background
        LinearGradient(
          gradient: Gradient(colors: [
            Color("BackgroundPrimary"),
            Color("BackgroundSecondary")
          ]),
          startPoint: .topLeading,
          endPoint: .bottomTrailing
        )
        .ignoresSafeArea()

        // Content
        ScrollView {
          VStack(spacing: 20) {
            // Header
            VStack(alignment: .leading, spacing: 8) {
              Text(String(localized: "home.header.title"))
                .font(.system(size: 28, weight: .bold, design: .default))
                .tracking(0.3)

              Text(String(localized: "home.header.subtitle"))
                .font(.system(size: 16, weight: .regular, design: .default))
                .foregroundColor(.secondary)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal, 16)
            .padding(.vertical, 20)

            // Items Grid
            VStack(spacing: 12) {
              if isLoading {
                LoadingView()
              } else if items.isEmpty {
                EmptyStateView()
              } else {
                ForEach(items) { item in
                  ItemCardView(item: item)
                }
              }
            }
            .padding(.horizontal, 16)
            .padding(.bottom, 20)
          }
        }
      }
      .navigationTitle(String(localized: "home.title"))
      .task {
        await loadItems()
      }
    }
  }

  @MainActor
  private func loadItems() async {
    isLoading = true
    defer { isLoading = false }
    do {
      try await Task.sleep(nanoseconds: 1_000_000_000) // Simulate network delay
      try Task.checkCancellation()
      items = Item.samples
    } catch is CancellationError {
      items = []
    } catch {
      items = []
    }
  }
}

// MARK: - Item Card Component
struct ItemCardView: View {
  let item: Item

  var body: some View {
    VStack(alignment: .leading, spacing: 12) {
      // Image/Icon
      RoundedRectangle(cornerRadius: 12)
        .fill(item.tint.opacity(0.2))
        .frame(height: 120)
        .overlay(
          Image(systemName: item.icon)
            .font(.system(size: 40))
            .foregroundColor(item.tint)
        )

      // Content
      VStack(alignment: .leading, spacing: 8) {
        HStack {
          VStack(alignment: .leading, spacing: 4) {
            Text(item.title)
              .font(.headline)
              .lineLimit(1)

            Text(item.description)
              .font(.caption)
              .foregroundColor(.secondary)
              .lineLimit(2)
          }

          Spacer()

          if item.isNew {
            BadgeView(text: String(localized: "home.item.badge.new"), color: item.tint)
          }
        }

        // Action Button
        Button(action: {}) {
          Text(String(localized: "home.item.details.button"))
            .font(.subheadline)
            .fontWeight(.semibold)
            .frame(maxWidth: .infinity)
            .frame(height: 36)
            .background(item.tint.opacity(0.1))
            .foregroundColor(item.tint)
            .cornerRadius(8)
        }
        .accessibilityLabel(String(localized: "home.item.details.button"))
        .accessibilityValue(Text(item.title))
      }
      .padding(12)
    }
    .background(Color("CardBackground"))
    .cornerRadius(16)
    .shadow(color: Color("ShadowColor").opacity(0.08), radius: 8, x: 0, y: 2)
  }
}

// MARK: - Badge Component
struct BadgeView: View {
  let text: String
  let color: Color

  var body: some View {
    Text(text)
      .font(.caption2)
      .fontWeight(.semibold)
      .foregroundColor(Color("OnAccent"))
      .padding(.horizontal, 8)
      .padding(.vertical, 4)
      .background(color)
      .cornerRadius(4)
  }
}

// MARK: - Loading State
struct LoadingView: View {
  var body: some View {
    VStack(spacing: 12) {
      ForEach(0..<3, id: \.self) { _ in
        SkeletonItemCard()
      }
    }
    .redacted(reason: .placeholder)
    .shimmering()
  }
}

struct SkeletonItemCard: View {
  var body: some View {
    VStack(alignment: .leading, spacing: 12) {
      RoundedRectangle(cornerRadius: 12)
        .fill(Color("SkeletonFill"))
        .frame(height: 120)

      VStack(alignment: .leading, spacing: 8) {
        RoundedRectangle(cornerRadius: 4)
          .fill(Color("SkeletonFill"))
          .frame(height: 16)

        RoundedRectangle(cornerRadius: 4)
          .fill(Color("SkeletonFill"))
          .frame(height: 12)
      }
      .padding(12)
    }
    .background(Color("CardBackground"))
    .cornerRadius(16)
  }
}

extension View {
  func shimmering() -> some View {
    modifier(ShimmeringModifier())
  }
}

struct ShimmeringModifier: ViewModifier {
  @State private var isShimmering = false
  @Environment(\.accessibilityReduceMotion) private var reduceMotion

  func body(content: Content) -> some View {
    Group {
      if reduceMotion {
        content
      } else {
        ZStack {
          content
            .opacity(isShimmering ? 0.6 : 1)

          LinearGradient(
            gradient: Gradient(colors: [.clear, Color("SkeletonHighlight").opacity(0.3), .clear]),
            startPoint: .topLeading,
            endPoint: .bottomTrailing
          )
          .offset(x: isShimmering ? 400 : -400)
        }
        .onAppear {
          withAnimation(.linear(duration: 1.5).repeatForever(autoreverses: false)) {
            isShimmering = true
          }
        }
      }
    }
  }
}

// MARK: - Empty State
struct EmptyStateView: View {
  var body: some View {
    VStack(spacing: 16) {
      Image(systemName: "list.bullet.circle")
        .font(.system(size: 48))
        .foregroundColor(.secondary)

      VStack(spacing: 4) {
        Text(String(localized: "home.empty.title"))
          .font(.headline)

        Text(String(localized: "home.empty.subtitle"))
          .font(.caption)
          .foregroundColor(.secondary)
      }

      Button(action: {}) {
        Text(String(localized: "home.empty.create"))
          .fontWeight(.semibold)
          .padding(.horizontal, 20)
          .padding(.vertical, 10)
          .background(Color("AccentColor"))
          .foregroundColor(Color("OnAccent"))
          .cornerRadius(8)
      }
    }
    .padding(32)
  }
}

// MARK: - Explore View
struct ExploreView: View {
  var body: some View {
    NavigationStack {
      Text(String(localized: "explore.placeholder"))
        .navigationTitle(String(localized: "explore.title"))
    }
  }
}

// MARK: - Profile View
struct ProfileView: View {
  var body: some View {
    NavigationStack {
      Text(String(localized: "profile.placeholder"))
        .navigationTitle(String(localized: "profile.title"))
    }
  }
}

// MARK: - Data Models
struct Item: Identifiable {
  let id = UUID()
  let title: String
  let description: String
  let icon: String
  let tintName: String
  let isNew: Bool
  var tint: Color { Color(tintName) }

  static let samples = [
    Item(
      title: String(localized: "home.item.swift.title"),
      description: String(localized: "home.item.swift.description"),
      icon: "swift",
      tintName: "ItemTintPrimary",
      isNew: true
    ),
    Item(
      title: String(localized: "home.item.design.title"),
      description: String(localized: "home.item.design.description"),
      icon: "paintpalette.fill",
      tintName: "ItemTintSecondary",
      isNew: false
    ),
    Item(
      title: String(localized: "home.item.performance.title"),
      description: String(localized: "home.item.performance.description"),
      icon: "speedometer",
      tintName: "ItemTintTertiary",
      isNew: true
    ),
  ]
}

// MARK: - Preview
#Preview {
  ContentView()
    .preferredColorScheme(.light)
}

#Preview("Dark Mode") {
  ContentView()
    .preferredColorScheme(.dark)
}

#Preview("Large Text") {
  ContentView()
    .environment(\.dynamicTypeSize, .xLarge)
}
